from users.models import User
from documents.models import Document

admin = User.objects.get(username='admin')

editor =User.objects.get(username='editor')

viewer = User.objects.get(username='viewer')

documents = [
    {
        'title': 'Business Plan 2026',
        'description': 'Company business plan for year 2026',
        'file_name': 'business_plan.pdf',
        'file_size': 204800,
        'minio_path': '',
        'status': 'stored',
        'uploaded_by': admin
    },
    {
        'title': 'Employee Handbook',
        'description': 'HR policies and employee guidelines',
        'file_name': 'employee_handbook.pdf',
        'file_size': 512000,
        'minio_path': '',
        'status': 'stored',
        'uploaded_by': admin
    },
    {
        'title': 'Q1 Financial Report',
        'description': 'Financial report for Q1 2026',
        'file_name': 'q1_report.pdf',
        'file_size': 102400,
        'minio_path': '',
        'status': 'stored',
        'uploaded_by': editor
    },
    {
        'title': 'Product Roadmap',
        'description': 'Product development roadmap for 2026',
        'file_name': 'roadmap.pdf',
        'file_size': 307200,
        'minio_path': '',
        'status': 'stored',
        'uploaded_by': editor
    },
    {
        'title': 'Marketing Strategy',
        'description': 'Digital marketing strategy document',
        'file_name': 'marketing.pdf',
        'file_size': 153600,
        'minio_path': '',
        'status': 'pending',
        'uploaded_by': admin
    },
]

for doc in documents:
    Document.objects.create(**doc)

print(f"Users created: {User.objects.count()}")
print(f"Documents created: {Document.objects.count()}")
print("Done!")
