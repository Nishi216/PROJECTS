from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt        #this is to allow the other domains to use API methods
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from EmployeeApp.models import Departments, Employees
from EmployeeApp.serializers import DepartmentSerializer, EmployeesSerializer

from django.core.files.storage import default_storage


#API FOR DEPARTMENT
@csrf_exempt
def departmentApi(request, id = 0):        #the method uses an optional id generally used for deleting
    if request.method=='GET':           #this will simply fetch the data from the table in JSON formatS
        departments = Departments.objects.all()     #this is getting all data from Departments table
        departments_serializer = DepartmentSerializer(departments, many = True)  #this is converting the data into JSON format
        return JsonResponse(departments_serializer.data, safe = False)

    elif request.method == 'POST':          #for inserting data into the table
        department_data = JSONParser().parse(request)       #parsing the JSON data first before serializing
        departments_serializer = DepartmentSerializer(data = department_data)
        if departments_serializer.is_valid():       #to check if model is valid, then save to database
            departments_serializer.save()
            return JsonResponse("Added Successfully!", safe= False)
        return JsonResponse("Failed to Add!", safe=False)
    
    elif request.method == 'PUT':
        department_data = JSONParser().parse(request)
        department = Departments.objects.get(DepartmentId = department_data['DepartmentId'])
        departments_serializer = DepartmentSerializer(department, data = department_data)
        if departments_serializer.is_valid():       #to check if model is valid, then save to database
            departments_serializer.save()
            return JsonResponse("Updated Successfully!", safe= False)
        return JsonResponse("Failed to Update!", safe=False)

    elif request.method == 'DELETE':
        department = Departments.objects.get(DepartmentId = id)
        department.delete()
        return JsonResponse("Deleted Successfully!", safe = False)


#API FOR EMPLOYEES
@csrf_exempt
def employeeApi(request, id = 0):        #the method uses an optional id generally used for deleting
    print("request", request )
    if request.method=='GET':           #this will simply fetch the data from the table in JSON format
        employees = Employees.objects.all()     #this is getting all data from Departments table
        employees_serializer = EmployeesSerializer(employees, many = True)  #this is converting the data into JSON format
        return JsonResponse(employees_serializer.data, safe = False)

    elif request.method == 'POST':          #for inserting data into the table
        employees_data = JSONParser().parse(request)       #parsing the JSON data first before serializing
        employees_serializer = EmployeesSerializer(data = employees_data)
        if employees_serializer.is_valid():       #to check if model is valid, then save to database
            employees_serializer.save()
            return JsonResponse("Added Successfully!", safe= False)
        return JsonResponse("Failed to Add!", safe=False)
    
    elif request.method == 'PUT':
        employee_data = JSONParser().parse(request)
        employee = Employees.objects.get(EmployeeId = employee_data['EmployeeId'])
        employee_serializer = EmployeesSerializer(employee, data = employee_data)
        if employee_serializer.is_valid():       #to check if model is valid, then save to database
            employee_serializer.save()
            return JsonResponse("Updated Successfully!", safe= False)
        return JsonResponse("Failed to Update!", safe=False)

    elif request.method == 'DELETE':
        employee = Employees.objects.get(DepartmentId = id)
        employee.delete()
        return JsonResponse("Deleted Successfully!", safe = False)


@csrf_exempt
def saveFile(request):
    file = request.FILES['myFile']
    file_name = default_storage.save(file.name, file)
    return JsonResponse(file_name, safe=False)
