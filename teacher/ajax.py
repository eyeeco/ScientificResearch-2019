# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.db.models import Q

from django.http import Http404
from django.utils import simplejson
from teacher.forms import *
from teacher.models import *
from teacher.utility import copyFundsummaryToBudget,copyBudgetToFundsummary
from const.models import *
from const import FINAL_WEB_CONFIRM 
from common.utils import  status_confirm
from backend.logging import logger, loginfo
from backend.decorators import check_auth
from django.template.loader import render_to_string
from adminStaff.models import ProjectSingle
from users.models import Special
@dajaxice_register 
def DeleteProject(request,pid):
    loginfo(pid)
    project=ProjectSingle.objects.get(pk=pid)
    project.delete()

@dajaxice_register
def ChangeSpecial(request,pid,value):
    value=int(value)
    project=ProjectSingle.objects.get(pk=pid)
    project.project_special=Special.objects.get(id=value)
    project.save()

@dajaxice_register
def achivementChange(request,form,achivementid,pid,is_submited):

    achivementform = ProjectAchivementForm(deserialize_form(form))
    projectsingle = ProjectSingle.objects.get(project_id=pid)
    finalsubmit = FinalSubmit.objects.get(project_id = projectsingle)
    message=""
    if achivementform.is_valid():
        achivementtitle = achivementform.cleaned_data["achivementtitle"]
        mainmember = achivementform.cleaned_data["mainmember"]
        introduction = achivementform.cleaned_data["introduction"]
        remarks = achivementform.cleaned_data["remarks"]
        achivementtype = achivementform.cleaned_data["achivementtype"]
        achivementtype=AchivementTypeDict.objects.get(achivementtype=achivementtype)
        if achivementid == 0:
            new_achivement = ProjectAchivement(achivementtitle=achivementtitle,mainmember=achivementtitle,introduction=introduction,remarks=remarks,
                achivementtype=achivementtype,project_id=projectsingle)
            new_achivement.save()
            message = u"新的研究成果添加成功"
            loginfo(p=achivementtitle,label="achivementtitle")
        else:
            old_achivement = ProjectAchivement.objects.get(content_id=achivementid)
            old_achivement.achivementtitle = achivementtitle
            old_achivement.mainmember = mainmember
            old_achivement.introduction = introduction
            old_achivement.remarks = remarks
            old_achivement.achivementtype = achivementtype
            old_achivement.save()
            message = u"修改成功"
    else:
        logger.info("achivementform Valid Failed"+"**"*10)
        logger.info(achivementform.errors)
        message = u"数据没有填完整，请重新填写"
    table = refresh_achivement_table(request,pid,is_submited) 
    ret={'table':table,'message':message,}
    return simplejson.dumps(ret)


def refresh_achivement_table(request,pid,is_submited):
    achivement_list = ProjectAchivement.objects.filter(project_id = pid)
    return render_to_string("widgets/finalreport/final_achivement_table.html",
                            {        
                                'pid':pid,
                                'achivement_list':achivement_list,
                                'is_submited':is_submited,
        })

@dajaxice_register
def achivementDelete(request,achivementid,pid,is_submited):
    projectsingle = ProjectSingle.objects.get(project_id=pid)
    delete_achivement = ProjectAchivement.objects.get(content_id = achivementid)
    delete_achivement.delete()
    table = refresh_achivement_table(request,pid,is_submited) 
    ret = {'message':u'删除成功','table':table}
    return simplejson.dumps(ret)

@dajaxice_register
def datastaticsChange(request,form,datastaticsid,pid,is_submited):

    datastaticsform = ProjectDatastaticsForm(deserialize_form(form))
    projectsingle = ProjectSingle.objects.get(project_id = pid)
    finalsubmit = FinalSubmit.objects.get(project_id=projectsingle)
    message=""
    if datastaticsform.is_valid():
        statics_num = datastaticsform.cleaned_data["statics_num"]
        staticstype = datastaticsform.cleaned_data["staticstype"]
        staticstype = StaticsTypeDict.objects.get(staticstype=staticstype)
        staticsdatatype = datastaticsform.cleaned_data["staticsdatatype"]
        staticsdatatype = StaticsDataTypeDict.objects.get(staticsdatatype=staticsdatatype)
        if datastaticsid == 0:
            new_staticsdata = ProjectStatistics(statics_num=statics_num,staticsdatatype=staticsdatatype,
                staticstype=staticstype,project_id=projectsingle)
            new_staticsdata.save()
            message = u"新的统计数据添加成功"
        else:
            old_staticsdata = ProjectStatistics.objects.get(content_id=datastaticsid)
            old_staticsdata.statics_num = statics_num
            old_staticsdata.staticstype = staticstype
            old_staticsdata.staticsdatatype = staticsdatatype
            old_staticsdata.save()
            message = u"修改成功"
    else:
        logger.info("datastaticsform Valid Failed"+"**"*10)
        logger.info(datastaticsform.errors)
        message = u"数据没有填完整，请重新填写"
    table = refresh_datastatics_table(request,pid,is_submited) 
    ret={'table':table,'message':message,}
    return simplejson.dumps(ret)

def refresh_datastatics_table(request,pid,is_submited):
    datastatics_list = ProjectStatistics.objects.filter(project_id = pid)
    return render_to_string("widgets/finalreport/final_datastatics_table.html",
                            {        
                                'pid':pid,
                                'datastatics_list':datastatics_list,
                                'is_submited':is_submited,
        })

@dajaxice_register
def datastaticsDelete(request,datastaticsid,pid,is_submited):
    delete_datastatics = ProjectStatistics.objects.get(content_id = datastaticsid)
    delete_datastatics.delete()
    table = refresh_datastatics_table(request,pid,is_submited) 
    ret = {'message':u'删除成功','table':table}
    return simplejson.dumps(ret)

@dajaxice_register
def staticsChange(request,statics_type):
    staticsdatatypedict = StaticsDataTypeDict.objects.filter(staticstype__staticstype = statics_type)
    staticsdatatype_set = []
    for temp in staticsdatatypedict:
        staticsdatatype_set.append(temp.staticsdatatype)
    ret={'staticsdatatype':staticsdatatype_set,}
    return simplejson.dumps(ret)

@dajaxice_register
def fundSummary(request, form,remarkmentform,pid,finance_account,is_submited):
    profundsummary = ProjectFundSummary.objects.get(project_id = pid) 
    profundsummaryform = ProFundSummaryForm(deserialize_form(form),instance = profundsummary)
    profundsummaryremarkmentform=ProFundSummaryRemarkmentForm(deserialize_form(remarkmentform),instance = profundsummary )
    project = ProjectSingle.objects.get(project_id = pid)
    flag = False
    if profundsummaryform.is_valid() and finance_account:
        total_budget = float(profundsummaryform.cleaned_data["total_budget"])
        total_expenditure =  float(profundsummaryform.cleaned_data["total_expenditure"])
        if total_budget < 0 or total_expenditure < 0:
            message = u"数据未填写完整或数据格式不对，保存失败"
        else:
            laborcosts_budget = float(profundsummaryform.cleaned_data["laborcosts_budget"])
            # if laborcosts_budget <= total_budget * 0.3:
            if total_budget <= project.project_budget_max:
                profundsummaryform.save()
                #copyFundsummaryToBudget(pid)
                project.finance_account=finance_account
                project.save()
                if is_submited:
                    if profundsummaryremarkmentform.is_valid():
                        profundsummaryremarkmentform.save()
                        message=u"保存成功"
                        flag = True
                        status_confirm(request,project)
                    else:
                        message=u"决算详细说明未填或字数超过限制"
                else:
                    message=u"保存成功"
            else:
                message = u"经费决算表总结额应低于项目最大预算金额,请仔细核实"
            # else:
            #     message = u"劳务费应低于总结额的30%,请仔细核实"
    else:
        loginfo(p=profundsummaryform.errors,label='profundsummaryform.errors')
        message = u"数据未填写完整或数据格式不对，保存失败"

    # table = refresh_fundsummary_table(request,profundsummaryform,pid)
    ret = {'message':message,'flag':flag}
    return simplejson.dumps(ret)

@dajaxice_register
def fundSummaryRemarkment(request,form,pid):
    profundsummary = ProjectFundSummary.objects.get(project_id = pid)
    profundsummaryremarkmentform = ProFundSummaryRemarkmentForm(deserialize_form(form),instance = profundsummary)
    if profundsummaryremarkmentform.is_valid():
        profundsummaryremarkmentform.save()
        message=u"保存成功"
    else:
        message=u"决算说明为必填项"
    ret ={'message':message}
    return simplejson.dumps(ret)

@dajaxice_register
def fundBudget(request, form, remarkmentform,pid,max_budget,projectcode,is_submited = False):
    profundbudget = ProjectFundBudget.objects.get(project_id = pid)
    profundbudgetform = ProFundBudgetForm(deserialize_form(form),instance = profundbudget)
    profundbudgetremarkmentform = ProFundBudgetRemarkmentForm(deserialize_form(remarkmentform),instance = profundbudget)
    project = ProjectSingle.objects.get(project_id = pid )
    flag = False
    identity = request.session.get('auth_role', "")
    accessList = [ADMINSTAFF_USER,SCHOOL_USER,FINANCE_USER]
    if not check_input(max_budget) or not check_input(projectcode):
        message = ""
        if not check_input(max_budget):
            message += u"项目最大预算不能为空 "
        if not check_input(projectcode):
            message += u"项目编号不能为空 "
        #if not check_input(finance_account):
        #   message += u"项目财务编号不能为空 "
        ret = {'message':message,'flag':flag,}
        return simplejson.dumps(ret)
    if identity in accessList:
        project.project_budget_max = max_budget
    project.project_code = projectcode
    #project.finance_account = finance_account
    project.save()
    if profundbudgetform.is_valid():
        total_budget = float(profundbudgetform.cleaned_data["total_budget"])
        if total_budget < 0:
            message = u"数据未填写完整或数据格式不对，保存失败"
        else:
            laborcosts_budget = float(profundbudgetform.cleaned_data["laborcosts_budget"])
            # if laborcosts_budget <= total_budget * 0.3:
            if total_budget <= project.project_budget_max:
                profundbudgetform.save()
                copyBudgetToFundsummary(pid)
                if is_submited:
                    if profundbudgetremarkmentform.is_valid():
                        profundbudgetremarkmentform.save()
                        flag = True
                        message=u"保存成功"
                        status_confirm(request,project)
                    else:
                        message="预算详细说明未填或字数超过限制"
                else:
                    message=u"保存成功"
            else:
                message = u"经费预算表总结额应低于项目最大预算金额,请仔细核实"
            # else:
            #     message = u"劳务费应低于总结额的30%,请仔细核实"
    else:
        loginfo(p=profundbudgetform.errors,label='profundbudgetform.errors')
        message = u"数据未填写完整或数据格式不对，保存失败"
    # table = refresh_fundsummary_table(request,profundsummaryform,pid)
    ret = {'message':message,'flag':flag,'project_code':project.project_code,'project_budget_max':project.project_budget_max,}
    return simplejson.dumps(ret)

@dajaxice_register
def fundBudgetRemarkment(request,form,pid):
    profundbudget = ProjectFundBudget.objects.get(project_id = pid)
    profundbudgetremarkmentform = ProFundBudgetRemarkmentForm(deserialize_form(form),instance = profundbudget)
    identity = request.session.get('auth_role', "")
    accessList = [ADMINSTAFF_USER,SCHOOL_USER,FINANCE_USER]
    if profundbudgetremarkmentform.is_valid():
        profundbudgetremarkmentform.save()
        message=u"保存成功"
    else:
        message=u"预算说明为必填项"
    ret = {'message':message}
    return simplejson.dumps(ret)

def check_input(inputStr):
    inputStr = str(inputStr)
    if inputStr == "None" or len(inputStr) == 0:
        return False
    else:
        return True

def refresh_fundsummary_table(request, profundsummaryform,pid):
    return render_to_string("widgets/finalreport/final_fundsummary_table.html",
                            {
                                'pid':pid,
                                'profundsummaryform':profundsummaryform,
        })

@dajaxice_register
def createProject(request, title, special):
    teacher = TeacherProfile.objects.get(userid = request.user)
    createNewProject(teacher, title, special)
    return simplejson.dumps({})
@dajaxice_register
def finalReportContent(request,pid,finalsubmitform,is_submited):
    final = FinalSubmit.objects.get( project_id = pid)
    final_form = FinalReportForm(deserialize_form(finalsubmitform),instance=final)
    if final_form.is_valid():
        final_form.save()
        go_next = True
    else:
        go_next = False
        finalsubmitform = refresh_finalsubmit_form(request,final_form,is_submited)
    ret = {'finalsubmitform':finalsubmitform,'go_next':go_next,}
    return simplejson.dumps(ret)

def refresh_finalsubmit_form(request,final_form,is_submited):

    return render_to_string("widgets/finalreport/finalreport_content.html",
                            {
                                'is_submited':is_submited,
                                'final':final_form,
        })

@dajaxice_register
def finalReportFinish(request,pid):
    project = ProjectSingle.objects.get(project_id = pid)
    finalsubmit = project.finalsubmit
    fundsummary = project.projectfundsummary
    loginfo(p=finalsubmit.project_summary,label="finalsubmit")
    loginfo(p=fundsummary.total_budget,label="fundbudget")
    if finalsubmit.project_summary:
        if fundsummary.total_budget != '0':
            status_confirm(request,project)
            status = '1'
            message = u"项目状态变为结题书网上提交"
        else:
            status = '0'
            message = u"请完善经费决算表内容"
    else:
        status = '0'
        message = u"请完善报告正文内容"

    ret = {'message':message,'pid':pid,'status':status,}
    return simplejson.dumps(ret)


@dajaxice_register
def saveProgress(request, pid, report_content):
    if report_content == "":
        return "empty input"
    project = ProjectSingle.objects.get(project_id = pid)
    current_year = datetime.datetime.today().year
    if ProgressReport.objects.filter(Q(project_id = pid) & Q(year = current_year)).count():
        ProgressReport.objects.get(Q(project_id = pid) & Q(year = current_year)).delete();
    report = ProgressReport(project_id = project, summary = report_content)
    report.save()
    return "ok"

@dajaxice_register
def refreshProgressHistory(request, pid):
    reports = ProgressReport.objects.filter(project_id = pid).order_by("-year")
    is_teacher = (request.session.get('auth_role') == TEACHER_USER) 
    return render_to_string("widgets/progress_history_table.html", {"reports": reports, "is_teacher": is_teacher, })

@dajaxice_register
def submitProgress(request, pid):
    project = ProjectSingle.objects.get(project_id = pid)
    is_redirect = (request.session.get('auth_role') == TEACHER_USER)
    current_year = datetime.datetime.today().year
    if not ProgressReport.objects.filter(Q(project_id = pid) & Q(year = current_year)).count():
        return simplejson.dumps({"message": "empty report"})
    status_confirm(request,project)
    return simplejson.dumps({"message": "ok", "is_redirect": is_redirect, "pid": pid})

@dajaxice_register
def changeProgress(request, report_id, report_content):
    if report_content == "":
        return "empty input"
    report = ProgressReport.objects.get(content_id = report_id)
    report.summary = report_content
    report.save()
    return "ok"
