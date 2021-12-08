from dlapi import DlApi
from models.report import ContractorReport, EmployeeReport, Report
from ui.form import Form

class ReportLogic():

  def __init__(self, dlapi: DlApi) -> None:
    self.dlapi = dlapi

  def new_employee_report(self, form: Form):
    rep = self.__parse_employee_form(form)
    report = self.dlapi.add_employee_report(rep)
    return self.__add_employee_extras(report)

  def new_contractor_report(self, form: Form):
    rep = self.__parse_contractor_form(form)
    report = self.dlapi.add_contractor_report(rep)
    return self.__add_contractor_extras(report)

  def get(self, id: int):
    report = self.dlapi.get_one_employee_report(id)
    if report is None:
      return
    return self.__add_employee_extras(report)

  def get_all(self):
    reports = self.dlapi.get_all_employee_reports()
    return [self.__add_employee_extras(rep) for rep in reports]

  def get_filtered(self, filter):
    reports = self.dlapi.get_filtered_employee_reports(filter)
    return [self.__add_employee_extras(rep) for rep in reports]

  def get_reports_for_task(self, task_id: int):
    filter = {'task_id': task_id}
    reports = self.dlapi.get_filtered_employee_reports(filter)
    return [self.__add_employee_extras(rep) for rep in reports]
  
  def get_reports_for_employee(self, employee_id: int):
    filter = {'employee_id': employee_id}
    reports = self.dlapi.get_filtered_employee_reports(filter)
    return [self.__add_employee_extras(rep) for rep in reports]
  
  def get_reports_for_contractor(self, contractor_id: int):
    filter = {'contractor_id': contractor_id}
    reports = self.dlapi.get_filtered_contractor_reports(filter)
    return [self.__add_contractor_extras(rep) for rep in reports]
  
  def get_reports_for_building(self, building_id: int):
    task_filter = {'building_id': building_id}
    tasks = self.dlapi.get_filtered_tasks(task_filter)
    reports = []
    for task in tasks:
      filter = {'task_id': task.id}
      reports.extend(self.dlapi.get_filtered_employee_reports(filter))
    return [self.__add_employee_extras(rep) for rep in reports]

  def __add_employee_extras(self, report: EmployeeReport):
    employee = self.dlapi.get_one_employee(report.employee_id)
    task = self.dlapi.get_one_task(report.id)
    building = self.dlapi.get_one_building(task.building_id)
    contractor_reports = self.dlapi.get_filtered_contractor_reports({'employee_report_id': report.id})
    report.add_employee(employee)
    report.add_task(task)
    report.add_building(building)
    report.add_contractor_reports(contractor_reports)
    return report

  def __add_contractor_extras(self, report: ContractorReport):
    contractor = self.dlapi.get_one_contractor(report.contractor_id)
    report.add_contractor(contractor)
    return report
  
  def __parse_employee_form(self, form: Form) -> EmployeeReport:
    ''' Returns instance of Report if everything is ok. '''
    try:
      id = form['id']
    except StopIteration:
      id = 0

    return EmployeeReport(
        id, 
        form['report_date'],
        form['approved'],
        form['description'],
        form['note'],
        form['hours'],
        form['employee_id'],
        form['task_id'],
        form['material_cost'],
        form['labor_cost'],
      )

  def __parse_contractor_form(self, form: Form) -> ContractorReport:
    ''' Returns instance of Report if everything is ok. '''
    try:
      id = form['id']
    except StopIteration:
      id = 0

    return ContractorReport(
        id, 
        form['report_date'],
        form['approved'],
        form['description'],
        form['note'],
        form['hours'],
        form['contractor_id'],
        form['employee_report_id'],
        form['contractor_fee'],
        form['contractor_rating'],
      )
