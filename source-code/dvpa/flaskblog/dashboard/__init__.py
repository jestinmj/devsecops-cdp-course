from flask import (Blueprint, request, redirect, render_template, url_for, session, flash)

dashboard = Blueprint('dashboard', __name__, template_folder='templates')