from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group,User
from django.shortcuts import render, redirect


# # Create your views here.
# from myapp.models import user_table
from lime import explanation

from myapp.models import user_table, water_table, feedback_table, Complaint_table


def login_get(request):
    return render(request,'login_page.html')

def adminhome(request):
    return render(request,'adminhome.html')

def logins_post(request):
    username=request.POST['uname']
    password=request.POST['pwrd']
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request, user)
        if user.groups.filter(name="admin").exists():
            return redirect('/myapp/adminhome/')
        elif user.groups.filter(name="user").exists():
            return redirect('/myapp/userhome')
        else:
            messages.error(request,"User Profile is not found")
            return redirect('/myapp/login_get/')
    else:
        messages.error(request,"Invalid username or password")
        return redirect('/myapp/login_get/')


def user_register_get(request):
    return render(request,'user_registeration.html')

def user_register_post(request):
    a=request.POST['name']
    b=request.POST['age']
    c=request.POST['phoneno']
    uname=request.POST['username']
    pwd=request.POST['password']
    if User.objects.filter(username=uname).exists():
        messages.warning(request,'username is already registered')
        return redirect('/myapp/user_register_get/')
    u=User.objects.create(username=uname,password=make_password(pwd))
    group=Group.objects.get(name='user')
    u.groups.add(group)
    u.save()
    f=user_table()
    f.name=a
    f.age=b
    f.phoneno=c
    f.LOGIN=u
    f.save()
    return redirect('/myapp/login_get/')


def view_user_register(request):
    a=user_table.objects.all()
    return render(request,'view_user.html',{'data':a})

def edituser(request,id):
    a=user_table.objects.get(id=id)
    request.session['id']=id
    return render(request,'edituser.html',{'data':a})

def edituserpost(request):
    a=request.POST['name']
    b=request.POST['age']
    c=request.POST['phoneno']
    f=user_table.objects.get(id=request.session['id'])
    f.name=a
    f.age=b
    f.phoneno=c
    f.save()
    return redirect('/myapp/view_user_register/')

def deleteuser(request,id):
    a=user_table.objects.get(id=id)
    a.delete()
    return redirect('/myapp/view_user_register/')


def waterquality(request):
    return render(request,'waterquality.html')

def waterqualitypost(request):
    a=float(request.POST['pH'])
    b=float(request.POST['Hardness'])
    c=float(request.POST['Solids'])
    d=float(request.POST['Chloramines'])
    e=float(request.POST['Sulfate'])

    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    import shap
    import matplotlib.pyplot as plt

    data = pd.read_csv(settings.BASE_DIR / 'dataset' / 'pH,Hardness,Solids,Chloramines.csv')
    x=data.drop('Potability',axis=1)
    y=data['Potability']

    x_train,x_test,y_train,y_test=train_test_split(
        x,y,test_size=0.2,random_state=42
    )

    model=RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(x_train,y_train)

    new_prediction=pd.DataFrame({
        'pH':[a],
        'Hardness':[b],
        'Solids':[c],
        'Chloramines':[d],
        'Sulfate':[e],
    })
    prediction=model.predict(new_prediction)[0]
    print("\n Prediction:",prediction)

    explainer=shap.Explainer(model)
    explanation=explainer(new_prediction)

    class_index = list(model.classes_).index(prediction)
    student_explanation = explanation[0, :, class_index].values

    shap_data = {}

    for feature, value in zip(
            new_prediction.columns,
            student_explanation
    ):
        shap_data[feature] = round(float(value), 4)

    shap_string = ""

    for feature, value in shap_data.items():
        shap_string = shap_string + feature + ": " + str(value) + ", "

    water_table.objects.create(
        pH=a,
        Hardness=b,
        Solids=c,
        Chloramines=d,
        Sulfate=e,
        predictionresult=prediction,
        featurecontribution=shap_string
    )

    return redirect('/myapp/viewresult/')


def viewresult(request):
    a=water_table.objects.all()
    return render(request,'result.html',{'data':a})

def feedback(request):
    return render(request,'feedback.html')

def feedbackpost(request):
    a=request.POST['message']
    b=feedback_table()
    b.message=a
    b.save()
    return redirect('/myapp/viewfeedback/')

def viewfeedback(request):
    a=feedback_table.objects.all()
    return render(request,'viewfeedback.html',{'data':a})

def replycomplaint(request,id):
    a=Complaint_table.objects.get(id=id)
    request.session['id']=id
    return render(request,'replycomplaint.html',{'data':a})

def replycomplaintpost(request):
    a=request.POST['complaintreply']
    b = Complaint_table.objects.get(id=request.session['id'])
    b.complaintreply = a
    b.save()
    return redirect('/myapp/viewcomplaint/')

def userhome(request):
    return render(request,'userhome.html')

def home(request):
    return render(request,'home.html')

def sendcomplaint(request):
    return render(request,'sendcompaint.html')

def complaintpost(request):
    a=request.POST['complaint']
    b=Complaint_table()
    b.complaint=a
    b.save()
    return redirect('/myapp/viewcomplaint/')

def viewcomplaint(request):
    a=Complaint_table.objects.all()
    return render(request,'viewcomplaint.html',{'data':a})


def editcomplaintpost(request):
    a=request.POST['complaint']
    f=Complaint_table.objects.get(id=request.session['id'])
    f.complaint=a
    f.save()
    return redirect('/myapp/viewcomplaint/')

def deletecomplaint(request,id):
    a=Complaint_table.objects.get(id=id)
    a.delete()
    return redirect('/myapp/viewcomplaint/')

def editcomplaint(request,id):
    a=Complaint_table.objects.get(id=id)
    request.session['id']=id
    return render(request,'editcomplaint.html',{'data':a})

def admin_view_complaints(request):
    a=Complaint_table.objects.all()
    return render(request,'admin_view_complaints.html',{'data':a})




