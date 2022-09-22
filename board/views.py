import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import connections
from .models import *
from .forms import *


def school_name_sql(school_id):
    cursor = connections['default'].cursor()
    cursor.execute('SELECT school FROM board_school WHERE id = %s', [school_id])
    school_name = cursor.fetchone()[0]
    cursor.close()
    return school_name


def board_name_sql(board_id):
    cursor = connections['default'].cursor()
    cursor.execute('SELECT board FROM board_board WHERE id = %s', [board_id])
    board_name = cursor.fetchone()[0]
    cursor.close()
    return board_name


# Create your views here.
def school(request):
    school_data = School.objects.raw('SELECT * FROM board_school')
    context = {'school_data': school_data}
    return render(request, 'board/school.html', context)


def school_create(request):
    if request.method == "POST":
        school_get = request.POST.get('school')
        cursor = connections['default'].cursor()
        cursor.execute('INSERT INTO board_school (school, created_at) VALUES (%s, %s)',
                       [school_get, datetime.datetime.now()])
        cursor.close()
        return redirect('school')
    return render(request, 'board/school_create.html')


def board(request, school_id):
    school_name = school_name_sql(school_id)
    board_data = Board.objects.raw('SELECT * FROM board_board WHERE school_id = %s', [school_id])
    context = {'board_data': board_data, 'school_id': school_id, 'school_name': school_name}
    return render(request, 'board/board.html', context)


def board_create(request, school_id):
    if request.method == "POST":
        board_get = request.POST.get('board')
        cursor = connections['default'].cursor()
        cursor.execute('INSERT INTO board_board (school_id, board, created_at) VALUES (%s, %s, %s)',
                       [school_id, board_get, datetime.datetime.now()])
        cursor.close()
        return redirect('board', school_id=school_id)
    context = {'school_id': school_id}
    return render(request, 'board/board_create.html', context)


def post(request, school_id, board_id):
    school_name = school_name_sql(school_id)
    board_name = board_name_sql(board_id)
    post_data = Post.objects.raw('SELECT * FROM board_post WHERE board_id = %s', [board_id])
    context = {'post_data': post_data, 'board_id': board_id, 'school_id': school_id, 'board_name': board_name,
               'school_name': school_name}
    return render(request, 'board/post.html', context)


@login_required
def post_create(request, school_id, board_id):
    if request.method == "POST":
        title_get = request.POST.get('title')
        content_get = request.POST.get('content')
        cursor = connections['default'].cursor()
        cursor.execute(
            'INSERT INTO board_post (board_id, title, content, created_at, author_id) VALUES (%s, %s, %s, %s, %s)',
            [board_id, title_get, content_get, datetime.datetime.now(), request.user.id])
        cursor.close()
        return redirect('post', school_id=school_id, board_id=board_id)
    context = {'school_id': school_id, 'board_id': board_id}
    return render(request, 'board/post_create.html', context)


def post_detail(request, school_id, board_id, post_id):
    school_name = school_name_sql(school_id)
    board_name = board_name_sql(board_id)
    post_data = Post.objects.filter(id=post_id).first()
    comment_data = Comment.objects.filter(post_id=post_id).all()
    context = {'post_data': post_data, 'board_id': board_id, 'school_id': school_id, 'board_name': board_name,
               'comment_data': comment_data,
               'school_name': school_name}
    return render(request, 'board/post_detail.html', context)


def post_delete(request, school_id, board_id, post_id):
    post_data = Post.objects.filter(id=post_id).first()
    if post_data.author_id == request.user.id:
        cursor = connections['default'].cursor()
        cursor.execute('DELETE FROM board_post WHERE id = %s', [post_id])
        cursor.close()
    return redirect('post', school_id=school_id, board_id=board_id)


@login_required
def comment_create(request, school_id, board_id, post_id):
    if request.method == "POST":
        content_get = request.POST.get('content')
        cursor = connections['default'].cursor()
        cursor.execute(
            'INSERT INTO board_comment (post_id, content, created_at, author_id) VALUES (%s, %s, %s, %s)',
            [post_id, content_get, datetime.datetime.now(), request.user.id])
        cursor.close()
    return redirect('post_detail', school_id=school_id, board_id=board_id, post_id=post_id)


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('school')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})
