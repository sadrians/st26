# Create your views here.

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

import util
import os
from django.template.loader import render_to_string

from sequencelistings.forms import SequenceListingForm, TitleForm, SequenceForm, FeatureForm, QualifierForm, MultipleFeatureForm

from models import SequenceListing, Title, Sequence, Feature, Qualifier

detailTemplate = 'sequencelistings/detail.html'
# detailTemplate = 'sequencelistings/detail1.html'

# class IndexView(generic.ListView):
#     template_name = 'sequencelistings/index.html'
#     context_object_name = 'sequencelistings'
#   
#     def get_queryset(self):
#         """Return all sequence listings."""
#         return SequenceListing.objects.all()

def index(request):
    sls = SequenceListing.objects.all()
    
    return render(request, 'sequencelistings/index.html', 
                   {'sequencelistings': sls})


# class DetailView(generic.DetailView):
#     model = SequenceListing
#     template_name = 'sequencelistings/detail.html'

def detail(request, pk): #good
    sl = get_object_or_404(SequenceListing, pk=pk)
        
    return render(request, detailTemplate, {'sequencelisting': sl})

def add_sequencelisting(request):
#     print 'add_sequencelisting invoked'
    if request.method == 'POST':
        form = SequenceListingForm(request.POST)
        title_form = TitleForm(request.POST)

        if form.is_valid() and title_form.is_valid():
            sl_instance = SequenceListing.objects.create(
            fileName = request.POST.get('fileName'),
            dtdVersion = '1',
            softwareName = 'prototype',
            softwareVersion = '0.1',
            productionDate = timezone.now(), #should be overwritten upon xml export
            
            applicantFileReference = request.POST.get('applicantFileReference'),
     
            IPOfficeCode = request.POST.get('IPOfficeCode'),
            applicationNumberText = request.POST.get('applicationNumberText'),
            filingDate = request.POST.get('filingDate'),
         
            earliestPriorityIPOfficeCode = request.POST.get('earliestPriorityIPOfficeCode'),
            earliestPriorityApplicationNumberText = request.POST.get('earliestPriorityApplicationNumberText'),
            earliestPriorityFilingDate = request.POST.get('earliestPriorityFilingDate'),
         
            applicantName = request.POST.get('applicantName'),
            applicantNameLanguageCode = request.POST.get('applicantNameLanguageCode'),
            applicantNameLatin = request.POST.get('applicantNameLatin'),
         
            inventorName = request.POST.get('inventorName'),
            inventorNameLanguageCode = request.POST.get('inventorNameLanguageCode'),
            inventorNameLatin = request.POST.get('inventorNameLatin'),
            )
            
            sl_instance.save()
            
            tcd = title_form.cleaned_data
            title_instance = Title(sequenceListing = sl_instance,
                inventionTitle = tcd['inventionTitle'],
                inventionTitleLanguageCode = tcd['inventionTitleLanguageCode']
                )
            
            title_instance.save()
            
            return HttpResponseRedirect(reverse('sequencelistings:detail', 
                                                args=(sl_instance.pk,)))
    else:
        form = SequenceListingForm()
        title_form = TitleForm()
        
    return render(request, 'sequencelistings/add_sequencelisting.html', 
                  {'form': form, 'title_form': title_form})

def add_title(request, pk):
#     print 'add_title invoked'
    if request.method == 'POST':
        form = TitleForm(request.POST)

        if form.is_valid():
            sl = SequenceListing.objects.get(pk=pk)
            cd = form.cleaned_data
            
            title_instance = Title(sequenceListing = sl,
                inventionTitle = cd['inventionTitle'].encode('utf-8'),
                inventionTitleLanguageCode = cd['inventionTitleLanguageCode']
                )
            title_instance.save()
            
            return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
    else:
        form = TitleForm()
    return render(request, 'sequencelistings/add_title.html', {'form': form, 'pk': pk})

def sequence(request, pk, spk):
    seq = Sequence.objects.get(pk=spk)
    form = SequenceForm(instance=seq, initial={'organism': seq.getOrganism()})
    form.organism = seq.getOrganism()
    featureFormDic = {}
    qualifierFormDic = {}
    for f in seq.feature_set.all():
        featureFormDic[f] = FeatureForm(instance=f, mt=seq.moltype, initial={'featureKey': f.featureKey})

        qualifierFormList = []
        for q in f.qualifier_set.all():
            qualifierFormList.append(QualifierForm(feature=f, 
                                                   instance=q, 
                                                   initial={'qualifierName': q.qualifierName}))

        qualifierFormDic[f] = qualifierFormList
            
#     if request.method == 'POST':
         
 
#         if form.is_valid():
#             cd = form.cleaned_data
#             
#             fk = cd['featureKey']
#             fl = cd['location']
#             f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
#             f.save()
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
#     else:
#         form = FeatureForm(mt=seq.moltype)
    return render(request, 'sequencelistings/sequence.html', {'form': form, 'seq': seq, 
                                                              'featureFormDic': featureFormDic, 
                                                              'qualifierFormDic': qualifierFormDic,})
def add_multiple_feature(request, pk, spk):
    #     print 'add_multiple_feature invoked'
    seq = Sequence.objects.get(pk=spk)
    if request.method == 'POST':
        form = MultipleFeatureForm(request.POST, moltype=seq.moltype)
 
        if form.is_valid():
            cd = form.cleaned_data
            
            fk = cd['featureKey']
            fl = cd['location']
            qn = cd['qualifierName']
            qv = cd['qualifierValue']
            
            if 'ra' in fl:
                locations = util.rangeFromString(fl) 
            else:
                locations = fl.split(',')
            for l in locations:
                f = Feature.objects.create(sequence=seq, featureKey=fk, location=l)
                f.save()
                q = Qualifier.objects.create(feature=f, 
                                             qualifierName = qn, 
                                             qualifierValue = qv)
                q.save()
             
            return HttpResponseRedirect(reverse('sequencelistings:detail', args=(seq.sequenceListing.pk,)))
    else:
        form = MultipleFeatureForm(request.POST, moltype=seq.moltype)
    return render(request, 'sequencelistings/add_multiple_feature.html', {'form': form})

# def add_multiple_feature(request, pk, spk):
#     #     print 'add_multiple_feature invoked'
#     seq = Sequence.objects.get(pk=spk)
#     if request.method == 'POST':
#         form = MultipleFeatureForm(request.POST, moltype=seq.moltype)
#  
#         if form.is_valid():
#             cd = form.cleaned_data
#             
#             fk = cd['featureKey']
#             fl = cd['location']
#             qn = cd['qualifierName']
#             qv = cd['qualifierValue']
#             
#             locations = fl.split(',')
#             for l in locations:
#                 f = Feature.objects.create(sequence=seq, featureKey=fk, location=l)
#                 f.save()
#                 q = Qualifier.objects.create(feature=f, 
#                                              qualifierName = qn, 
#                                              qualifierValue = qv)
#                 q.save()
#              
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(seq.sequenceListing.pk,)))
#     else:
#         form = MultipleFeatureForm(request.POST, moltype=seq.moltype)
#     return render(request, 'sequencelistings/add_multiple_feature.html', {'form': form})
    
def add_sequence(request, pk):
#     print 'add_sequence invoked'
    if request.method == 'POST':
        organism = request.POST.get('organism')
        form = SequenceForm(request.POST)

        if form.is_valid():
            sl = SequenceListing.objects.get(pk=pk)
            cd = form.cleaned_data
            
            sequence_instance = Sequence(sequenceListing = sl,
                length = len(cd['residues']),
                moltype = cd['moltype'],
                residues = cd['residues'] 
                )
            
            sequence_instance.save()
            
            value_for_source = 'source'
            if cd['moltype'] == 'AA':
                value_for_source = 'SOURCE'
                
            value_for_organism = 'organism'
            if cd['moltype'] == 'AA':
                value_for_organism = 'ORGANISM'
                
            value_for_moltype = 'mol_type'
            if cd['moltype'] == 'AA':
                value_for_moltype = 'MOL_TYPE'
            
            feature_instance = Feature.objects.create(sequence=sequence_instance, 
                                                      featureKey=value_for_source, 
                                                      location='1..%s' % sequence_instance.length)
            feature_instance.save()
            
            organism_qualifier_instance = Qualifier.objects.create(feature=feature_instance, 
                                                          qualifierName=value_for_organism, 
                                                          qualifierValue=organism)
            organism_qualifier_instance.save()
            
            mol_type_qualifier_instance = Qualifier.objects.create(feature=feature_instance, 
                                                          qualifierName=value_for_moltype, 
                                                          qualifierValue=util.MOL_TYPE_QUALIFIER_VALUES[cd['moltype']])
            mol_type_qualifier_instance.save()
            
            return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
    else:
        form = SequenceForm()
    return render(request, 'sequencelistings/add_seq.html', {'form': form, 'pk': pk})

def add_feature(request, pk, spk):
    seq = Sequence.objects.get(pk=spk)
     
    if request.method == 'POST':
        form = FeatureForm(request.POST, mt=seq.moltype)
 
        if form.is_valid():
            cd = form.cleaned_data
             
            fk = cd['featureKey']
            fl = cd['location']
            f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
            f.save()
            return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
    else:
        form = FeatureForm(mt=seq.moltype)
    return render(request, 'sequencelistings/add_feature.html', {'form': form})

def add_qualifier(request, pk, spk, fpk):
#     print 'add_qualifier invoked'
    f = Feature.objects.get(pk=fpk)
    if request.method == 'POST':
        form = QualifierForm(request.POST, feature=f)

        if form.is_valid():
            qn = request.POST.get('qualifierName')
            qv = request.POST.get('qualifierValue')
            q = Qualifier.objects.create(feature=f, qualifierName=qn, qualifierValue=qv)
            q.save()
            return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
    else:
        form = QualifierForm(feature=f)
    return render(request, 'sequencelistings/add_qualifier.html', 
                  {'form': form, 
                   'pk': pk, 
                   'spk': spk, 
                   'fpk': fpk})

def generateXml(request, pk):
        sl = SequenceListing.objects.all().get(pk=pk)
        
        xmlFilePath = helper_generateXml(sl)
        
        return render(request, 'sequencelistings/xmloutput.html', 
                      {'outputfilepath': xmlFilePath, 
                       'location': os.path.abspath(xmlFilePath)})
        
def helper_generateXml(sl):
        sl.productionDate = timezone.now()
        sl.save()
        sequences = sl.sequence_set.all()
     
        xml = render_to_string('xml_template.xml', {'sequenceListing': sl,
                                                    'sequences': sequences
                                                    }).encode('utf-8', 'strict')
 
        outf = os.path.join(util.PROJECT_DIRECTORY,
                            'sequencelistings',
                            'static',
                            'sequencelistings',
                            '%s.xml' % sl.fileName)
         
        with open(outf, 'w') as gf:
            gf.write(xml) 
         
        xmlFilePath = 'sequencelistings/%s.xml' % sl.fileName
         
        return xmlFilePath















# def add_feature(request, pk, spk):
#     seq = Sequence.objects.get(pk=spk)
#     
#     if request.method == 'POST':
#         form = FeatureForm(request.POST)
# 
#         if form.is_valid():
#             cd = form.cleaned_data
#             
#             fk = cd['featureKey']
#             fl = cd['location']
#             f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
#             f.save()
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
#     else:
#         form = FeatureForm()
#     return render(request, 'sequencelistings/add_feature.html', {'form': form})


# def sequence(request, pk, spk):
#     seq = Sequence.objects.get(pk=spk)
#     form = SequenceForm(instance=seq)
#     form.organism = seq.getOrganism()
#     featureFormList = []
#     for f in seq.feature_set.all():
#         featureFormList.append(FeatureForm(instance=f))
#         
# #     if request.method == 'POST':
#         
# 
# #         if form.is_valid():
# #             cd = form.cleaned_data
# #             
# #             fk = cd['featureKey']
# #             fl = cd['location']
# #             f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
# #             f.save()
# #             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
# #     else:
# #         form = FeatureForm(mt=seq.moltype)
#     return render(request, 'sequencelistings/sequence.html', {'form': form, 'seq': seq, 
#                                                               'featureFormList': featureFormList})



# def edit_feature(request, fpk):
#     feature = get_object_or_404(Feature, id=fpk)
#     print feature
#     form = FeatureForm(request.POST or None, mt=feature.sequence.moltype, instance=feature)
#     print form
#     if form.is_valid():
#         form.save()
#         
#         return HttpResponseRedirect(reverse('sequencelistings:detail', 
#                                             args=(feature.sequence.sequenceListing.pk,)))
#     else:
#         form = FeatureForm(mt=feature.sequence.moltype)
#     return render(request, 'sequencelistings/edit_feature.html', {'form': form})




# def add_sequence(request, pk):
# #     print 'add_sequence invoked'
#     if request.method == 'POST':
#         organism = request.POST.get('organism')
#         form = SequenceForm(request.POST)
# 
#         if form.is_valid():
#             sl = SequenceListing.objects.get(pk=pk)
#             cd = form.cleaned_data
#             
#             sequence_instance = Sequence(sequenceListing = sl,
#                 length = len(cd['residues']),
#                 moltype = cd['moltype'],
#                 residues = cd['residues'] 
#                 )
#             
#             sequence_instance.save()
#             
#             
#             feature_instance = Feature.objects.create(sequence=sequence_instance, 
#                                                       featureKey='source', 
#                                                       location='1..%s' % sequence_instance.length)
#             feature_instance.save()
#             
#             organism_qualifier_instance = Qualifier.objects.create(feature=feature_instance, 
#                                                           qualifierName='organism', 
#                                                           qualifierValue=organism)
#             organism_qualifier_instance.save()
#             
#             mol_type_qualifier_instance = Qualifier.objects.create(feature=feature_instance, 
#                                                           qualifierName='mol_type', 
#                                                           qualifierValue=util.MOL_TYPE_QUALIFIER_VALUES[cd['moltype']])
#             mol_type_qualifier_instance.save()
#             
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
#     else:
#         form = SequenceForm()
#     return render(request, 'sequencelistings/add_seq.html', {'form': form, 'pk': pk})


# def index(request): #good
#     sls = SequenceListing.objects.all()
#     print sls
#     return render(request, 'sequencelistings/index.html', {'sequencelistings': sls})
#  
# def detail(request, sequenceListing_id): #good
#     print 'detail invoked'
#     sl = get_object_or_404(SequenceListing, pk=sequenceListing_id)
#        
#     return render(request, 'sequencelistings/detail.html', {'sequencelisting': sl})
# def index(r):
#     return HttpResponse('Hello world. You are at the sequence listing index.')
   
# def detail(request, sequenceListing_id):
#     return HttpResponse("You're looking at poll %s." % sequenceListing_id)


# def add_feature(request, pk, spk): #good
#     print 'add_feature invoked'
#     seq = Sequence.objects.get(pk=spk)
#     print 'sequenceIdNo: ', seq.sequenceIdNo
#     print 'moltype: ', seq.moltype
#     
#     if request.method == 'POST':
#         form = FeatureForm(request.POST)
# #         assert False
#         if form.is_valid():
#             cd = form.cleaned_data
#             
#             fk = cd['featureKey']
#             fl = cd['location']
#             f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
#             f.save()
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
#     else:
#         form = FeatureForm()
#     return render(request, 'sequencelistings/add_feature.html', {'form': form})

# def add_feature(request, pk, spk):
#     print 'add_feature invoked'
# #     s = Sequence.objects.all().get(pk=int(spk))
#     if request.method == 'POST':
#         
#         form = FeatureForm(request.POST, s.moltype)
# 
#         if form.is_valid():
#             cd = form.cleaned_data
#             seq = Sequence.objects.get(pk=spk)
#             fk = cd['featureKey']
#             fl = cd['location']
# 
# #             fk = request.POST.get('featureKey')
# #             fl = request.POST.get('location')
#             f = Feature.objects.create(sequence=seq, featureKey=fk, location=fl)
#             f.save()
#             return HttpResponseRedirect(reverse('sequencelistings:detail', args=(pk,)))
#     else:
#         form = FeatureForm(s.moltype)
#     return render(request, 'sequencelistings/add_feature.html', {'form': form})
    # {% url 'sequencelistings:add_feature' %}
    
# def generateXml(request, pk):
# #     print 'generateXml invoked'
#     sl = SequenceListing.objects.all().get(pk=pk)
#     sl.productionDate = timezone.now()
#     sl.save()
#     o = 'sequencelistings/%s' % sl.generateXml()
#     location = os.path.abspath(o)
#     return render(request, 'sequencelistings/xmloutput.html', 
#                   {'outputfilepath': o, 
#                    'location': location})
# 
# def generateXml1(request, pk):
#         sl = SequenceListing.objects.all().get(pk=pk)
#         sl.productionDate = timezone.now()
#         sl.save()
#         sequences = sl.sequence_set.all()
#     
#         xml = render_to_string('xml_template.xml', {'sequenceListing': sl,
#                                                     'sequences': sequences
#                                                     })
# 
#         outf = os.path.join(util.PROJECT_DIRECTORY,
#                             'sequencelistings',
#                             'static',
#                             'sequencelistings',
#                             'generated1_%s.xml' % sl.fileName)
#         
#         with open(outf, 'w') as gf:
#             gf.write(xml) 
#         
#         o = 'sequencelistings/generated1_%s.xml' % sl.fileName
#         
#         location = os.path.abspath(o)
#         return render(request, 'sequencelistings/xmloutput.html', 
#                       {'outputfilepath': o, 
#                        'location': location})



# from django.shortcuts import render, get_object_or_404
# from django.template.loader import render_to_string
#  
# from django.http import HttpResponse
# from sequencelistings.models import SequenceListing, Title, Sequence, Feature, Qualifier 
# 
# from django.utils import timezone
# import os 
# import util 
# 
# def index(request):
#     # Construct a dictionary to pass to the template engine as its context.
#     # Note the key boldmessage is the same as {{ boldmessage }} in the template!
#     context_dict = {'boldmessage': "I am bold font from the context"}
#     sequenceListings = SequenceListing.objects.all()
#     print 'sequenceListings', sequenceListings
#     # Return a rendered response to send to the client.
#     # We make use of the shortcut function to make our lives easier.
#     # Note that the first parameter is the template we wish to use.
# 
#     return render(request, 'sequencelistings/index.html', {'sequenceListings': sequenceListings})
# 
# def detail(request, pk): #good
#     sl = get_object_or_404(SequenceListing, pk=pk)
#         
#     return render(request, 'sequencelistings/detail.html', {'sequenceListing': sl})
# 
# 
# def about(request):
# #     return HttpResponse("Creator says here is the about page.")
#     # Construct a dictionary to pass to the template engine as its context.
#     # Note the key boldmessage is the same as {{ boldmessage }} in the template!
#     context_dict = {'boldmessage': "I am about bold font from the context"}
# 
#     # Return a rendered response to send to the client.
#     # We make use of the shortcut function to make our lives easier.
#     # Note that the first parameter is the template we wish to use.
# 
#     return render(request, 'sequencelistings/about.html', context_dict)
# 
# def xmloutput(request, pk):
#         sl = SequenceListing.objects.all().get(pk=pk)
#         
#         xmlFilePath = helper_generateXml(sl)
#         
#         return render(request, 'sequencelistings/xmloutput.html', 
#                       {'outputfilepath': xmlFilePath, 
#                        'location': os.path.abspath(xmlFilePath)})
#         
# def helper_generateXml(sl):
#         sl.productionDate = timezone.now()
#         sl.save()
#         sequences = sl.sequence_set.all()
#      
#         xml = render_to_string('xml_template.xml', {'sequenceListing': sl,
#                                                     'sequences': sequences
#                                                     }).encode('utf-8', 'strict')
#  
#         outf = os.path.join(util.PROJECT_DIRECTORY,
#                             'sequencelistings',
#                             'static',
#                             'sequencelistings',
#                             '%s.xml' % sl.fileName)
#          
#         with open(outf, 'w') as gf:
#             gf.write(xml) 
#          
#         xmlFilePath = 'sequencelistings/%s.xml' % sl.fileName
#          
#         return xmlFilePath
