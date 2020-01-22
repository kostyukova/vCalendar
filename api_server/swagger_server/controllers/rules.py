
from datetime import date

import connexion
import swagger_server.controllers.ErrorApiResponse as ErrorApiResponse
import swagger_server.dao.employee_dao as employee_dao
import swagger_server.dao.leave_days_dao as dao
from sqlalchemy import text
from swagger_server import util
from swagger_server.models.conflict_detail import ConflictDetail
from swagger_server.models.employee import Employee
from swagger_server.models.leave_days import LeaveDays
from swagger_server.models.leave_days_ex import LeaveDaysEx
from swagger_server.orm import Employee as Employee_orm
from swagger_server.orm import Employee_leave_days as LeaveDays_orm


'''
 - Only one BA engineer
 - Only one engineer from a team
 - Only three employee on vacation at the same time
 - Only one team leader
 - Only one O365
 - Only two Core
 - Only one OACI
'''


def check_rules(employee_id: int, start_date: date, end_date: date, id: int = None):
    kwargs = {"employee_id": employee_id, "start_date": start_date,
              "end_date": end_date, "id": id}
    result = [check_rules_1(**kwargs),
              check_rules_2(**kwargs),
              check_rules_3(**kwargs),
              check_rules_4(**kwargs),
              check_rules_5(**kwargs),
              check_rules_6(**kwargs),
              check_rules_7(**kwargs),
              ]
    return [elem for elem in result if elem]


def check_rules_1(employee_id: int, start_date: date, end_date: date, id: int = None):
    # check current employee is BA engineer
    if 'BA' not in get_employee_specs(employee_id):
        return None

    def rule(x): return x.filter(Employee_orm.specialization.like('%BA%'))
    found = dao.find_by_rule(start_date, end_date, rule, id)
    if len(found) > 0:
        dto = [to_dto(elem) for elem in found]
        return ConflictDetail(rule="Only one BA engineer", conflict_with_leave_days=dto)
    return None


def check_rules_2(employee_id: int, start_date: date, end_date: date, id: int = None):
    # check current employee is an engineer
    employee = employee_dao.get(employee_id)
    if 'team leader' == employee.position:
        return None

    def rule(x): return x.filter(Employee_orm.position != 'team leader')\
        .filter(Employee_orm.team_id == employee.team_id)
    found = dao.find_by_rule(start_date, end_date, rule, id)

    if len(found) > 0:
        dto = [to_dto(elem) for elem in found]
        return ConflictDetail(rule="Only one engineer from a team", conflict_with_leave_days=dto)
    return None


def check_rules_3(employee_id: int, start_date: date, end_date: date, id: int = None):
    def rule(x): return x
    found = dao.find_by_rule(start_date, end_date, rule, id)
    if len(found) > 2:
        dto = [to_dto(elem) for elem in found]
        return ConflictDetail(rule="Only three employee on vacation at the same time", conflict_with_leave_days=dto)
    return None


def check_rules_4(employee_id: int, start_date: date, end_date: date, id: int = None):
    # check current employee is a team leader
    employee = employee_dao.get(employee_id)
    if 'team leader' != employee.position:
        return None

    def rule(x): return x.filter(Employee_orm.position == 'team leader')
    found = dao.find_by_rule(start_date, end_date, rule, id)

    if len(found) > 0:
        dto = [to_dto(elem) for elem in found]
        return ConflictDetail(rule="Only one team leader", conflict_with_leave_days=dto)
    return None


def check_rules_5(employee_id: int, start_date: date, end_date: date, id: int = None):
    # check current employee is O365 engineer
    if 'O365' not in get_employee_specs(employee_id):
        return None

    def rule(x): return x.filter(Employee_orm.specialization.like('%O365%'))
    found = dao.find_by_rule(start_date, end_date, rule, id)
    if len(found) > 0:
        dto = [to_dto(elem) for elem in found]
        return ConflictDetail(rule="Only one O365", conflict_with_leave_days=dto)
    return None


def check_rules_6(employee_id: int, start_date: date, end_date: date, id: int = None):
    # check current employee is BA engineer
    if 'Core' not in get_employee_specs(employee_id):
        return None

    def rule(x): return x.filter(Employee_orm.specialization.like('%Core%'))
    found = dao.find_by_rule(start_date, end_date, rule, id)
    if len(found) > 1:
        dto = [to_dto(elem) for elem in found]
        return ConflictDetail(rule="Only two Core", conflict_with_leave_days=dto)
    return None


def check_rules_7(employee_id: int, start_date: date, end_date: date, id: int = None):
    # check current employee is BA engineer
    if 'OACI' not in get_employee_specs(employee_id):
        return None

    def rule(x): return x.filter(Employee_orm.specialization.like('%OACI%'))
    found = dao.find_by_rule(start_date, end_date, rule, id)
    if len(found) > 0:
        dto = [to_dto(elem) for elem in found]
        return ConflictDetail(rule="Only one OACI", conflict_with_leave_days=dto)
    return None


def get_employee_specs(employee_id: int):
    employee = employee_dao.get(employee_id)
    return employee.specialization.split(',')


def to_dto(found: LeaveDays_orm):
    employee = found.employee
    return LeaveDaysEx(id=found.id, employee_id=found.employee_id, leave_days=found.leave_days,
                       start_date=found.start_date, end_date=found.end_date,
                       employee=Employee(employee_id=employee.employee_id, full_name=employee.full_name,
                                         position=employee.position, specialization=employee.specialization,
                                         team_id=employee.team_id, expert=employee.expert, email=employee.email))
