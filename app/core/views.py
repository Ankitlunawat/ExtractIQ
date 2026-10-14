import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from .models import ExtractionJob
from .services import csv_safe

@login_required
def extract(request):
    jobs=ExtractionJob.objects.filter(owner=request.user).order_by("-created_at")
    return render(request,"extract.html",{"jobs":jobs,"section":"extract","total":jobs.count(),"records":sum(j.records.count() for j in jobs),"completed":jobs.filter(state="completed").count(),"rejected":sum(j.rejected for j in jobs)})

@login_required
def results(request,pk):
    job=get_object_or_404(ExtractionJob,pk=pk,owner=request.user)
    rows=job.records.order_by("title")
    q=request.GET.get("q","");rating=request.GET.get("rating","")
    if q:rows=rows.filter(title__icontains=q)
    if rating in ["1","2","3","4","5"]:rows=rows.filter(rating=int(rating))
    return render(request,"results.html",{"job":job,"records":rows,"section":"extract","q":q,"rating":rating,"ratings":[1,2,3,4,5]})

@login_required
def extract_export(request,pk,format):
    job=get_object_or_404(ExtractionJob,pk=pk,owner=request.user)
    fields=["title","url","price","currency","rating","available"]
    rows=list(job.records.values(*fields))
    if format=="json":
        response=JsonResponse(rows,safe=False);response["Content-Disposition"]='attachment; filename="extraction.json"';return response
    if format!="csv":return HttpResponse(status=404)
    response=HttpResponse(content_type="text/csv");response["Content-Disposition"]='attachment; filename="extraction.csv"'
    writer=csv.writer(response);writer.writerow(fields)
    for row in rows:writer.writerow([csv_safe(row[f]) for f in fields])
    return response
