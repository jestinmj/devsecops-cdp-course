from . import dashboard
from .post import *
from .password_change import *
from .profile import *


dashboard.add_url_rule('/dashboard/', view_func=List.as_view('index'))
dashboard.add_url_rule('/dashboard/page/<int:page>/', view_func=List.as_view('page'))
dashboard.add_url_rule('/dashboard/post/create/', view_func=CreatPost.as_view('create'))
dashboard.add_url_rule('/dashboard/post/edit/<slug>/', view_func=EditPost.as_view('edit'))
dashboard.add_url_rule('/dashboard/post/delete/<slug>/', view_func=DeletePost.as_view('delete'))
dashboard.add_url_rule('/dashboard/post/import-export/', view_func=ExportPost.as_view('import_export_post'))
dashboard.add_url_rule('/dashboard/download', view_func=ExportFileDownload.as_view('export_download'))
dashboard.add_url_rule('/dashboard/user/<int:uid>', view_func=ProfileInformation.as_view('profile_information'))
dashboard.add_url_rule('/dashboard/password-change', view_func=PasswordChange.as_view('password_change'))