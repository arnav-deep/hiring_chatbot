from typing import List, Optional
from pydantic import BaseModel

from connection import connection


class SearchQuery(BaseModel):
    is_full_time: Optional[bool] = False
    is_part_time: Optional[bool] = False
    full_time_salary: Optional[str] = None
    part_time_salary: Optional[str] = None
    skills: List[str] = []


def run_query(search_query: SearchQuery):
    with connection.cursor() as cursor:
        sql = (
            "SELECT DISTINCT mu.* "
            "FROM MercorUsers mu "
            "JOIN MercorUserSkills mus ON mu.userId = mus.userId "
            "JOIN Skills s ON mus.skillId = s.skillId WHERE"
        )

        if search_query.is_full_time is not None:
            sql += f" mu.fullTime = {bool(search_query.is_full_time)} AND"
        if search_query.is_part_time is not None:
            sql += f" mu.partTime = {bool(search_query.is_part_time)} AND"
        if search_query.is_full_time and search_query.full_time_salary is not None:
            sql += f" mu.fullTimeSalary <= {search_query.full_time_salary} AND"
        if search_query.is_part_time and search_query.part_time_salary is not None:
            sql += f" mu.partTimeSalary <= {search_query.part_time_salary} AND"

        if search_query.skills:
            sql += " s.skillValue IN ("
            for skill in search_query.skills:
                sql += f"'{skill.lower().strip()}',"
            sql = sql[:-1] + ") AND"

        sql = sql[:-4]
        cursor.execute(sql)
        result = cursor.fetchmany(5)
        if result:
            return result
    return None
