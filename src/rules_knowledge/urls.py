from django.urls import path
from rules_knowledge.views import (
    # DocumentType
    DocumentTypeCreateAPI,
    DocumentTypeListAPI,
    DocumentTypeDetailAPI,
    DocumentTypeUpdateAPI,
    DocumentTypeDeleteAPI,
    # VisaType
    VisaTypeCreateAPI,
    VisaTypeListAPI,
    VisaTypeDetailAPI,
    VisaTypeUpdateAPI,
    VisaTypeDeleteAPI,
    # VisaRuleVersion
    VisaRuleVersionCreateAPI,
    VisaRuleVersionListAPI,
    VisaRuleVersionDetailAPI,
    VisaRuleVersionUpdateAPI,
    VisaRuleVersionDeleteAPI,
    # VisaRequirement
    VisaRequirementCreateAPI,
    VisaRequirementListAPI,
    VisaRequirementDetailAPI,
    VisaRequirementUpdateAPI,
    VisaRequirementDeleteAPI,
    # VisaDocumentRequirement
    VisaDocumentRequirementCreateAPI,
    VisaDocumentRequirementListAPI,
    VisaDocumentRequirementDetailAPI,
    VisaDocumentRequirementUpdateAPI,
    VisaDocumentRequirementDeleteAPI,
)

app_name = 'rules_knowledge'

urlpatterns = [
    # DocumentType endpoints
    path('document-types/', DocumentTypeListAPI.as_view(), name='document-type-list'),
    path('document-types/create/', DocumentTypeCreateAPI.as_view(), name='document-type-create'),
    path('document-types/<uuid:id>/', DocumentTypeDetailAPI.as_view(), name='document-type-detail'),
    path('document-types/<uuid:id>/update/', DocumentTypeUpdateAPI.as_view(), name='document-type-update'),
    path('document-types/<uuid:id>/delete/', DocumentTypeDeleteAPI.as_view(), name='document-type-delete'),
    
    # VisaType endpoints
    path('visa-types/', VisaTypeListAPI.as_view(), name='visa-type-list'),
    path('visa-types/create/', VisaTypeCreateAPI.as_view(), name='visa-type-create'),
    path('visa-types/<uuid:id>/', VisaTypeDetailAPI.as_view(), name='visa-type-detail'),
    path('visa-types/<uuid:id>/update/', VisaTypeUpdateAPI.as_view(), name='visa-type-update'),
    path('visa-types/<uuid:id>/delete/', VisaTypeDeleteAPI.as_view(), name='visa-type-delete'),
    
    # VisaRuleVersion endpoints
    path('visa-rule-versions/', VisaRuleVersionListAPI.as_view(), name='visa-rule-version-list'),
    path('visa-rule-versions/create/', VisaRuleVersionCreateAPI.as_view(), name='visa-rule-version-create'),
    path('visa-rule-versions/<uuid:id>/', VisaRuleVersionDetailAPI.as_view(), name='visa-rule-version-detail'),
    path('visa-rule-versions/<uuid:id>/update/', VisaRuleVersionUpdateAPI.as_view(), name='visa-rule-version-update'),
    path('visa-rule-versions/<uuid:id>/delete/', VisaRuleVersionDeleteAPI.as_view(), name='visa-rule-version-delete'),
    
    # VisaRequirement endpoints
    path('visa-requirements/', VisaRequirementListAPI.as_view(), name='visa-requirement-list'),
    path('visa-requirements/create/', VisaRequirementCreateAPI.as_view(), name='visa-requirement-create'),
    path('visa-requirements/<uuid:id>/', VisaRequirementDetailAPI.as_view(), name='visa-requirement-detail'),
    path('visa-requirements/<uuid:id>/update/', VisaRequirementUpdateAPI.as_view(), name='visa-requirement-update'),
    path('visa-requirements/<uuid:id>/delete/', VisaRequirementDeleteAPI.as_view(), name='visa-requirement-delete'),
    
    # VisaDocumentRequirement endpoints
    path('visa-document-requirements/', VisaDocumentRequirementListAPI.as_view(), name='visa-document-requirement-list'),
    path('visa-document-requirements/create/', VisaDocumentRequirementCreateAPI.as_view(), name='visa-document-requirement-create'),
    path('visa-document-requirements/<uuid:id>/', VisaDocumentRequirementDetailAPI.as_view(), name='visa-document-requirement-detail'),
    path('visa-document-requirements/<uuid:id>/update/', VisaDocumentRequirementUpdateAPI.as_view(), name='visa-document-requirement-update'),
    path('visa-document-requirements/<uuid:id>/delete/', VisaDocumentRequirementDeleteAPI.as_view(), name='visa-document-requirement-delete'),
]

