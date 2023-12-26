# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models



class Bill(models.Model):
    bid = models.AutoField(db_column='BID', primary_key=True)  # Field name made lowercase.
    bdate = models.IntegerField(db_column='BDate')  # Field name made lowercase.
    byear = models.IntegerField(db_column='BYear')  # Field name made lowercase.
    bmonth = models.IntegerField(db_column='BMonth')  # Field name made lowercase.
    cusid = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='CUSID', blank=True, null=True)  # Field name made lowercase.
    current_reading = models.IntegerField(db_column='Current_Reading')  # Field name made lowercase.
    prev_reading = models.IntegerField(db_column='Prev_Reading')  # Field name made lowercase.
    bamount = models.IntegerField(db_column='Bamount')  # Field name made lowercase.
    # branch = models.ForeignKey('Branch', on_delete=models.CASCADE, db_column='Branch', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=200,
                              choices=[('Paid','Paid'),
                                ('Due', 'Due')], null=True)

    class Meta:
        managed = True
        db_table = 'bill'

    def __str__(self):
        return self.cusid.fullname


class Branch(models.Model):
    branch_id = models.AutoField(db_column='Branch_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=200,
                              choices=[('Paid','Paid'),
                                ('Due', 'Due')], null=True)  # Field name made lowercase.

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = 'branch'


class Customer(models.Model):
    scno = models.IntegerField(db_column='SCNO')  # Field name made lowercase.
    cusid = models.AutoField(db_column='CUSID', primary_key=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FullName', max_length=255)  # Field name made lowercase.
    dob = models.DateField(db_column='DateOfBirth', blank=True, null=True)
    address = models.CharField(db_column='Address', max_length=255)  # Field name made lowercase.
    mobileno = models.CharField(db_column='MobileNo', max_length=10)  # Field name made lowercase.
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='Branch_ID', blank=True, null=True)  # Field name made lowercase.
    demand_type = models.ForeignKey('Demandtype', on_delete=models.CASCADE, db_column='Demand_type_ID', blank=True,
                                    null=True, default="Free")  # Field name made lowercase.

    def __str__(self) -> str:
        return str(f"{self.cusid}--{self.fullname}")

    class Meta:
        managed = True
        db_table = 'customer'


class Demandrate(models.Model):
    drid = models.AutoField(db_column='DRID', primary_key=True)  # Field name made lowercase.
    demand_type = models.ForeignKey('Demandtype', models.DO_NOTHING, db_column='Demand_Type_ID', blank=True, null=True)  # Field name made lowercase.
    rate = models.IntegerField(blank=True, null=True)
    iscurrent = models.IntegerField(db_column='IsCurrent', blank=True, null=True)  # Field name made lowercase.
    effective_date = models.DateField(db_column='Effective_date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'demandrate'

class Demandtype(models.Model):
    demand_type_id = models.AutoField(db_column='Demand_Type_ID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'demandtype'

    def __str__(self) -> str:
        return self.description


class PaymentCus(models.Model):
    pid = models.AutoField(db_column='PID', primary_key=True)  # Field name made lowercase.
    bid = models.ForeignKey(Bill, on_delete=models.CASCADE, db_column='BID', blank=True, null=True)  # Field name made lowercase.
    pdate = models.DateField(db_column='PDate', blank=True, null=True)  # Field name made lowercase.
    pamount = models.IntegerField(db_column='PAmount', blank=True, null=True)  # Field name made lowercase.
    payment_type = models.ForeignKey('PaymentOption', on_delete=models.CASCADE, db_column='Payment_type_ID', blank=True, null=True)  # Field name made lowercase.
    rebate_amt = models.IntegerField(db_column='Rebate_Amt', blank=True, null=True)  # Field name made lowercase.
    fine_amt = models.IntegerField(db_column='Fine_Amt', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=200, 
                              choices=[('Paid','Paid'),
                                ('Due', 'Due')], null=True)
    class Meta:
        managed = True
        db_table = 'payment'
    
    def __str__(self)-> str:
        return str(f"{self.pid}--{self.bid}")


class PaymentOption(models.Model):
    poid = models.AutoField(db_column='POID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'payment_option'

    def __str__(self) -> str:
        return str(f"{self.poid}--{self.name}")