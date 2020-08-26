# -*- coding: utf-8 -*-
from odoo import models , fields , api
import time
from datetime import datetime, date, time, timedelta



from dateutil.relativedelta import relativedelta

class cmms_line(models.Model):
    _name='cmms.line'
    _description='Production lines'

    name=fields.Char(string='Production line', required='True')
    code=fields.Char(string='Line reference',required='True')
    Location=fields.Char(string='Location')
    sequence=fields.Integer(string='Sequence')

class cmms_equipment(models.Model):
    _name='cmms.equipment'
    _description='cmms maintenance equipements'

    name=fields.Char(string='name',required=True)
    type_eq=fields.Char(string='Unit of work reference', size=64 , required=True)

#g1
    line_id=fields.Many2one('cmms.line','Production line')
    local_id=fields.Many2one('stock.location', 'Location')
    startingdate=fields.Datetime('Starting date')
#g2

    vendor=fields.Many2one("res.partner","Vendor",required=True)
    trademark=fields.Char(string='trademark')
    active=fields.Boolean(string='active',default=True)
    description=fields.Text('description')
    u_ins=fields.Text(string='Usage instructions')

    s_info=fields.Text(string='Safety information')

    cmms_eq_ids=fields.Many2many(
       'product.product',
       string="test"
    )
    #PM
    Technician=fields.Many2one('res.users', 'Technician')
    begin_date = fields.Datetime(string="Begun date")
    end_date= fields.Datetime(string="End date")
    interval = fields.Integer(string="Interval",default=0)
    periodic = fields.Boolean(string="Periodic", default=False)
    next_pm= fields.Datetime(string="Next Preventive Maintenance")
    value_to_add=fields.Integer(string="value to add",default=0)

    @api.model
    @api.onchange('periodic')
    def make_it_zero(self):
        self.interval=0


    @api.one
    def calcul_Next_PM(self):
        if(self.periodic==False):
            d=fields.Datetime.from_string(self.begin_date)
            delta=timedelta(days=self.interval)
            result=d+delta
            
            c1=(fields.Datetime.from_string(self.end_date)-fields.Datetime.from_string(result))
            if (c1.total_seconds()>=0): 
                 
                self.next_pm=result
            else:
                self.next_pm=self.end_date

        else:
            d=fields.Datetime.from_string(self.begin_date)
            self.value_to_add=self.value_to_add+self.interval
            delta=timedelta(days=self.value_to_add)
            result=d+delta
            
            c1=(fields.Datetime.from_string(self.end_date)-fields.Datetime.from_string(result))
            if (c1.total_seconds()>=0): 
                 
                self.next_pm=result
            else:
                self.next_pm=self.end_date




class cmms_piece(models.Model):
    _inherit='product.product'
    _description='piece of change'


    cmms_piece_ids=fields.Many2many(
        'cmms.equipment',
        string="piece of change"
    )


class cmms_intervention(models.Model):
    _name='cmms.intervention'
    _description='CMMS intervention requests'
    name=fields.Char(string='name', required=True)
    Sender=fields.Many2one('res.users', 'Sender')
    Recipient=fields.Many2one('res.users', 'Recipient')
    machine=fields.Many2one("cmms.equipment","Machine")
    sc_date=fields.Date(string="Scheduled date")
    duration=fields.Datetime(string="Duration")



    int_priority=fields.Selection([('p0', 'Very Low'), ('p1', 'Low'), ('p2', 'Normal'), ('p3', 'High')],string='Priority')
    status=fields.Selection([('b','Breakdown'),('w','Working')],string="Status")
    type_inter=fields.Selection([('t0', 'Check'), ('t1', 'Repair'), ('t2', 'Revision'), ('t3', 'Other')], string='Type of intervention')
    motif=fields.Text(string="Motif")
    obsv=fields.Text(string="Observation")

class cmms_failure(models.Model):
    _name='cmms.failure'
    _description='CMMS failure list'
    name=fields.Char(string='name', required=True)
    desc=fields.Text(string='Desciption of failure')


class cmms_task(models.Model):
    _name='cmms.task'
    _description='CMMS Task list'
    name=fields.Char(string='name', required=True)
    desc=fields.Text(string='Desciption of Task')
    done=fields.Boolean(string='Done ?',default=False)



#work order
class cmms_wr(models.Model):
    _name='cmms.wr'
    _description='CMMS work orders'
    name=fields.Char(string="name",required=True)
    Order_by=fields.Many2one('res.users', 'Order by')
    machine = fields.Many2one("cmms.equipment", "Machine")
    failure_type=fields.Many2one('cmms.failure', 'Failure',required=True)
    Technician=fields.Many2one('res.users', 'Order to-Technician')
    int_priority=fields.Selection([('p0', 'Very Low'), ('p1', 'Low'), ('p2', 'Normal'), ('p3', 'High')],string='Priority')
    Reference_to=fields.Selection([('r1', 'Intervention Request'),('r2', 'Task')],string='Reference',required=True)
    notes=fields.Text(string='Notes')
    s_INT=fields.Many2one('cmms.intervention', 'Intervention Request')
    task=fields.Many2one("cmms.task","Task")
    #page: PM






    #added later
    sc_date=fields.Datetime(string="Scheduled date",default=datetime.now())
    sp_date=fields.Datetime(string="Until",default=datetime.now())
    uptime=fields.Float(string="Maintenance duration")
    @api.model
    @api.onchange('sc_date','sp_date')
    def _calcul_duration(self):
        #if (self.state == 'finished'):

            #now =datetime.now()

        timedelta = fields.Datetime.from_string(self.sp_date) - fields.Datetime.from_string(self.sc_date)

        self.uptime = timedelta.total_seconds() / 3600

        #else:
         #   self.uptime = 0
        


    state=fields.Selection([
            ('concept', 'Concept'),
            ('started', 'Started'),
            ('progress', 'In progress'),
            ('finished', 'Done'),
            ],default='concept')
    #This function is triggered when the user clicks on the button 'Set to concept'
    @api.one
    def concept_progressbar(self):
        self.write({
            'state': 'concept',
        })

    #This function is triggered when the user clicks on the button 'Set to started'
    @api.one
    def started_progressbar(self):
        self.write({
        'state': 'started'
        })

    #This function is triggered when the user clicks on the button 'In progress'
    @api.one
    def progress_progressbar(self):
        self.write({
        'state': 'progress'
        })

    #This function is triggered when the user clicks on the button 'Done'
    @api.one
    def done_progressbar(self):
        self.write({
        'state': 'finished',
        })





