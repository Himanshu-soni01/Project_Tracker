from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponse, Http404
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import sqlite3
import os

conn = sqlite3.connect('project_details.db')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        project_name TEXT,
        description TEXT,
        start_date TEXT,
        end_date TEXT,
        team_member TEXT,
        resource BYTEA
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS user(
        username TEXT NOT NULL UNIQUE,
        password TEXT,
        project TEXT
    )
''')
conn.commit()


def index(request):

    conn = sqlite3.connect('project_details.db')
    cur = conn.cursor()
    query = ('''SELECT project_name,description,start_date,end_date,resource FROM projects''')
    cur.execute(query)

    result = cur.fetchall()
    print(result)

    # query = ('SELECT project_name from projects')

    # cur.execute(query, ())

    # result = cur.fetchall()

    conn.close()

    if result:
        var = {
            'details': result,
        }
        return render(request, 'admin.html', var)

    var = {
        'projects': ['None']
    }
    return render(request, 'admin.html', var)


def users(request):
    return render(request, 'Users.html')


def usersignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        conn = sqlite3.connect('project_details.db')
        cur = conn.cursor()

        data = (username, password, '')
        query = ('INSERT INTO user values(?,?,?)')
        cur.execute(query, data)
        conn.commit()

        conn.close()

        return render(request, 'userlogin.html')
    return render(request, 'usersignup.html')


def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        conn = sqlite3.connect('project_details.db')
        cur = conn.cursor()

        query = ('SELECT password FROM user where username=(?)')
        cur.execute(query, (username,))

        result = cur.fetchone()

        conn.close()

        var = {
            'username': username,
        }

        if result is not None and result[0] == password:

            conn = sqlite3.connect('project_details.db')
            cur = conn.cursor()

            query = ('''SELECT project_name,description,start_date,end_date,resource FROM projects
                     where projects.team_member=?''')
            cur.execute(query,(username,))

            result = cur.fetchall()
            print(result)

            if result:
                var = {
                    'username':username,
                    'details': result,
                }
                return render(request, 'afterlogin.html', var)

            else:
                return render(request, 'afterlogin.html')

        else:
            error_message = 'Invalid username or password.'
            return render(request, 'userlogin.html', {'error': error_message})

    return render(request, 'userlogin.html')


def logout(request):
    return HttpResponse("Logout Successfully")


def projects(request):
    return render(request, 'projects.html', {'projects': projects})


def CreateProject(request):

    conn = sqlite3.connect('project_details.db')
    cur = conn.cursor()

    query = ('SELECT username FROM user')
    cur.execute(query)

    result = cur.fetchall()
    conn.close()

    res = []
   
    for i in result:
        res.append(i[0])

    var = {
        "members": res,
    }

    if request.method == 'POST':
        project_name = request.POST.get('project-name')
        description = request.POST.get('description')
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        selected_user = request.POST.get('selected-user')
        resources = request.FILES['resources']

        resources_name = resources.name

        fs = FileSystemStorage(location='D:\Project\Files')
        
        file_name = fs.save(resources_name, resources)
        
        conn = sqlite3.connect('project_details.db')
        cur = conn.cursor()

        data = (project_name, description, start_date,
                end_date, selected_user,resources_name)
        query = ('INSERT INTO projects values (?,?,?,?,?,?)')

        cur.execute(query, data)

        query = "UPDATE user SET project = ? WHERE username = ?"
        parameters = (project_name, selected_user)
        cur.execute(query, parameters)

        conn.commit()

        return render(request, 'admin.html')
    
    return render(request, 'CreateProject.html', var)

def download_file(request, file_path):

    file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_full_path):
        with open(file_full_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_full_path)}"'
            return response
    else:
        raise Http404("File does not exist.")
    

def update_project(request, project_name):

    conn = sqlite3.connect('project_details.db')
    cur = conn.cursor()

    query = '''SELECT project_name, description, start_date, end_date, resource FROM projects WHERE project_name = ?'''
    cur.execute(query, (project_name,))
    project_details = cur.fetchone()

    conn.close()

    var = {
        'project': project_details,
    }

    if request.method == 'POST':

        description = request.POST.get('description',None)
        start_date = request.POST['start_date']
        print(start_date)
        end_date = request.POST['end_date']
        print(end_date)
        resources = request.FILES['resources',None] if 'resources' in request.FILES else None

        conn = sqlite3.connect('project_details.db')
        cur = conn.cursor()

        query = '''UPDATE projects SET description = ?, start_date = ?, end_date = ?, resource = ? WHERE project_name = ?'''
        data = (description, start_date, end_date, resources, project_name)
        cur.execute(query, data)

        conn.commit()
        conn.close()

        return render(request, 'admin.html',var)
    
    return render(request, 'update_project.html', var)

