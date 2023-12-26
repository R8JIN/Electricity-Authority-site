from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import datetime
from billing.models import PaymentCus, Branch, PaymentOption, Demandtype, Demandrate, Customer, Bill
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from paypalrestsdk import Payment
from django.conf import settings
import paypalrestsdk


# Create your views here.


def payment_options(request, id):
    print(id)
    if request.method == "POST":
        option = request.POST['Option']
        if option == 'Paypal':
            print(option)
            return redirect('/paypal/initiate/%d/' % id)


def create_payment(request, id):
    paypalrestsdk.configure(
        mode=settings.PAYPAL_MODE,
        client_id=settings.PAYPAL_CLIENT_ID,
        client_secret=settings.PAYPAL_CLIENT_SECRET
    )
    bill = Bill.objects.get(bid=id)
    payment = Payment({
        'intent': 'sale',
        'payer': {
            'payment_method': 'paypal'
        },
        'redirect_urls': {
            'return_url': 'http://localhost:8000/paypal/execute/%d/' % id,
            'cancel_url': 'http://localhost:8000/paypal/cancel/'
        },
        'transactions': [{
            'amount': {
                'total': bill.bamount,
                'currency': 'USD'
            },
            "description": f"This is the payment transaction for  ."}
        ]
    })
    print(payment.create())
    if payment.create():
        for link in payment.links:
            if link.rel == 'approval_url':
                redirect_url = link.href
                return redirect(redirect_url)
    else:

        return HttpResponse("Payment Failed")


def execute_payment(request, id):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    paypalrestsdk.configure(
        mode=settings.PAYPAL_MODE,
        client_id=settings.PAYPAL_CLIENT_ID,
        client_secret=settings.PAYPAL_CLIENT_SECRET
    )
    payment = Payment.find(payment_id)
    if payment.execute({'payer_id': payer_id}):
        bill = Bill.objects.get(bid=id)
        bill.status = 'Paid'
        bill.save()
        pay = PaymentCus(bid=bill, pdate=datetime.datetime.now(), pamount=bill.bamount, status='Paid')
        # Payment executed successfully
        pay.save()
        return HttpResponse('Payment executed successfully.')
    else:
        return HttpResponse('Payment execution failed.')


def createSuperUser(request):  # SuperUser Registration Manually
    if request.method == 'POST':
        username = request.POST["un"]
        email = request.POST["email"]
        u = User(username=username, email=email)
        u.set_password(request.POST['pass'])
        u.is_superuser = True
        u.is_staff = True
        u.save()
        return render(request, "index.html", {})
    return render(request, "registration.html", {})


def login(request):  # Login for admin, user, superadmin
    if request.method == "POST":
        user = request.POST['user']
        password = request.POST['pass']
        user = auth.authenticate(username=user, password=password)
        if user is not None and user.is_staff:
            auth.login(request, user)
            return render(request, 'index.html', {})
        elif user is not None:
            auth.login(request, user)
            return render(request, 'user\\UserSearch.html', {})
        return HttpResponse("Login Error")


def logout(request):  # Logout
    auth.logout(request)
    return redirect('Home')


def createstaffuser(request):  # Superadmin can create staff users
    if request.method == "POST":
        user = request.POST['un']
        password = request.POST['pass']
        permission = request.POST.getlist('permission')
        try:
            if request.user.is_superuser:
                u = User(username=user)
                u.set_password(password)
                u.is_staff = True
                u.save()
                for p in permission:
                    for app_config in apps.get_app_configs():
                        try:
                            model = app_config.get_model(p)
                        except LookupError:
                            pass
                    content = ContentType.objects.get_for_model(model)
                    post_permission = Permission.objects.filter(content_type=content)
                    for per in post_permission:
                        u.user_permissions.add(per)
            return HttpResponse("Staff User created")
        except PermissionDenied:
            return HttpResponse("Permission Denied")
    return render(request, "staff\\createstaffuser.html", {})


def createuser(request):  # SuperAdmin and admin can create user
    if request.method == "POST":
        user = request.POST['un']
        password = request.POST['pass']

        if request.user.is_superuser or request.user.is_staff:
            u = User(username=user)
            u.set_password(password)
            u.is_staff = False
            u.is_superuser = False
            u.save()
        return HttpResponse("User created")

    return render(request, "user\\createuser.html", {})


def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return render(request, 'index.html', {})
        else:
            return render(request, 'user\\UserSearch.html', {})
    return render(request, 'index.html', {})


def view_branch(request):  # Branch insertion
    if request.method == "POST":
        name = request.POST['BName']
        status = request.POST['flexRadioDefault']
        form = Branch(name=name, status=status)

        form.save()
        return HttpResponse("Form Valid")
    return render(request, 'Branch.html', {})


def view_payment(request):  # PayemntOption Insertion
    if request.method == 'POST':
        name = request.POST['PNAME']
        status = request.POST['PaymentOptionStatus']
        form = PaymentOption(name=name, status=status)

        form.save()
        return HttpResponse("Form Valid")
    return render(request, 'Payment.html', {})


def view_demandtype(request):  # Demand Type Insertion
    if request.method == 'POST':
        description = request.POST['describe']
        status = request.POST['DemandTypeStatus']
        form = Demandtype(description=description, status=status)
        form.save()
        return HttpResponse('Form valid')
    return render(request, 'DemandType.html', {})


def view_demandrate(request):  # Demand Rate Insertion
    demand = Demandtype.objects.all()
    if request.method == 'POST':
        demand_type = request.POST['Demandtype']
        rate = request.POST['Rate']
        iscurrent = request.POST['isCurrent']  # Field name made lowercase.
        effective_date = request.POST['Date']  # Field name made lowercase.
        form = Demandrate(demand_type=Demandtype.objects.get(description=demand_type), rate=rate,
                          effective_date=effective_date, iscurrent=iscurrent)
        form.save()
        return HttpResponse('Form Valid')
    context = {'demandType': demand}
    return render(request, 'DemandRate.html', context)


def view_customer(request):  # Customer Insertion
    branch_id = Branch.objects.all()
    demand = Demandtype.objects.all()
    context = {'branch': branch_id,
               'demandtype': demand
               }
    if request.method == 'POST':
        scno = request.POST['scno']
        fullname = request.POST['CName']
        address = request.POST['Address']
        mobileno = request.POST['Contact']
        branch = request.POST['Branch']
        demand_type = request.POST['DemandRate']
        form = Customer(scno=scno, fullname=fullname, address=address, mobileno=mobileno,
                        branch=Branch.objects.get(branch_id=branch),
                        demand_type=Demandtype.objects.get(description=demand_type))
        form.save()
        return HttpResponse('Form Valid')
    return render(request, 'Customer.html', context)


def view_bill(request):  # Bill Insertion
    if request.method == 'POST':
        bdate = request.POST['BDate']
        byear = request.POST['BYear']
        bmonth = request.POST['BMonth']
        cusid = request.POST['CusID']
        current_reading = request.POST['CReading']
        previous_reading = request.POST['CPrevious']
        bamount = request.POST['BAmount']
        form = Bill(bdate=bdate, byear=byear, bmonth=bmonth, cusid=Customer.objects.get(cusid=cusid),
                    current_reading=current_reading, prev_reading=previous_reading, bamount=bamount)
        form.save()
        return HttpResponse("Form Valid")
    return render(request, 'bill.html', {})


def dopay(request):  # Payment Insertion
    payoption = PaymentOption.objects.all()
    if request.method == 'POST':
        pid = request.POST['pid']
        bid = request.POST['bid']
        pdate = request.POST['pdate']
        pamount = request.POST['pname']
        payment_t = request.POST['paydo']

        rebate_amt = request.POST['rebate']
        fine_amt = request.POST['fine']

        pay = PaymentCus(pid=pid, bid=Bill.objects.get(bid=bid),
                         pdate=pdate, pamount=pamount,
                         payment_type=PaymentOption.objects.get(poid=payment_t),
                         rebate_amt=rebate_amt, fine_amt=fine_amt)
        pay.save()
        return HttpResponse("Form Valid")
    content = {'paymenttype': payoption}
    return render(request, 'DoPay.html', content)


@login_required
def search(request):
    pay_option = PaymentOption.objects.all()
    print(pay_option)
    if request.method == 'POST':
        cus_id = request.POST['CUSID']
        try:
            obj = Customer.objects.get(cusid=cus_id)
            bill = Bill.objects.filter(cusid__cusid=cus_id)
            print(bill)

            payment = PaymentCus.objects.filter(bid__cusid=cus_id)

            context = {'Customer': obj, 'Bill': bill, 'Payment': payment, }
            return render(request, 'details.html', context)
        except ObjectDoesNotExist:
            return HttpResponse("Exception: data not found")


@login_required
def customerSearch(request):
    pay_option = PaymentOption.objects.all()

    try:
        if request.method == 'POST':
            phone = request.POST['phone']
            name = request.POST['name']
            dob = request.POST['dob']
            cus = Customer.objects.get(fullname=name, mobileno=phone, dob=dob)
            bill = Bill.objects.filter(cusid__cusid=cus.cusid)
            payment = PaymentCus.objects.filter(bid__cusid=cus)
            # print(payment)
            return render(request, 'user\\UserSearch.html',
                          {'cus': cus, 'bill': bill, 'payment': payment, 'options': pay_option})
    except ObjectDoesNotExist:
        return HttpResponse("Exception: Data not found")
    return render(request, 'user\\UserSearch.html', {})


@login_required
def report(request):
    if request.user.is_superuser and request.user.is_staff:
        return render(request, 'Report.html', {})


def customer_per_branch(request):
    customer = Customer.objects.all().order_by('branch')
    branch = Branch.objects.all()
    bill = Bill.objects.filter(status='Due').order_by('cusid__branch')
    print(bill)
    context = {'customer': customer, 'branch': branch, 'bill': bill}
    return render(request, 'staff\\CustomerPerBranch.html', context)


def customer_per_bill(request):
    branch = Branch.objects.all()
    customer = Customer.objects.all().order_by('branch')
    bill = Bill.objects.filter(status='Due').order_by('cusid__branch')
    context = {'branch': branch, 'bill': bill, 'customer': customer}
    return render(request, 'staff\\CustomerPerBill.html', context)


def customer_by_paymentmethod(request):
    payoptions = PaymentOption.objects.all()
    pay = PaymentCus.objects.all().order_by('payment_type')
    mydict = {}
    mylist = []
    for payop in payoptions:
        mydict.update({payop.name: []})
        for p in pay:
            if payop == p.payment_type:
                mydict[payop.name].append(p.bid.cusid.fullname)
        mydict[payop.name] = [*set(mydict[payop.name])]
    mylist.append(mydict)
    context = {'pay': pay, 'payoptions': payoptions, 'customer': mydict}
    return render(request, 'staff\\CustomerByPayOption.html', context)


def customer_by_demandtype(request):
    demand_type = Demandtype.objects.all()
    customer = Customer.objects.all().order_by('demand_type')
    context = {'demand_type': demand_type, 'customer': customer}
    return render(request, 'staff\\CustomerByDemandType.html', context)


def totalbill_branch(request):
    branch = Branch.objects.all()
    customer = Customer.objects.all().order_by('branch')
    bill = Bill.objects.filter(status='Due').order_by('cusid__branch', 'cusid')
    mydict = {}
    for br in branch:
        mydict.update({br.name: {}})
        for c in customer:
            amount = 0
            if c.branch == br:
                mydict[br.name].update({c.fullname: 0})
                for b in bill:
                    if b.cusid.branch == br and b.cusid == c:
                        amount = amount + b.bamount
                mydict[br.name][c.fullname] = amount
    context = {'branch': branch, 'bill': bill, 'dict': mydict}
    return render(request, 'staff\\totalAmtBranch.html', context)


def totalbill_year(request):
    year = Bill.objects.values('byear').distinct()
    bill = Bill.objects.filter(status='Due').order_by('-byear')
    mydict = {}
    for y in year:
        amount = 0
        mydict.update({y['byear']:0})
        for b in bill:
            if b.byear == y['byear']:
                amount = amount + b.bamount
        mydict[y['byear']] = amount
    context = {'dict': mydict}
    return render(request, 'staff\\TotalAmountByYear.html', context)
