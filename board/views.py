from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Boards,BoardComment,PurchaseHistory,GoodBoard,StoreBoard
from django.http import HttpResponse,JsonResponse
from recommend_system.models import BrowsingHistory,SearchHistory
from recommend_system import views as recommend_system
from accounts.models import Users,PointsHistory
from django.db.models import Q
from room.models import RoomJoining,Rooms
from django.utils import timezone
from notification.models import Notification
# Create your views here.

class TopPageBoardView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):

        try:
            board_list_from_recommend_system = recommend_system.create_recommend_board_list(request)
            selected_board_list = Boards.objects.filter(board_id__in = board_list_from_recommend_system)
            recommend_board_list = []
            for index,_ in enumerate(board_list_from_recommend_system):
                for _1 in selected_board_list:
                    if board_list_from_recommend_system[index] == _1.board_id:
                        recommend_board_list.append(_1)


        except:
            recommend_board_list = Boards.objects.all().order_by('created_at').reverse()[:10]

        latest_board_list = Boards.objects.exclude(posted_by_id=request.user.user_id).values()[:20]

        board_list = Boards.objects.all().values('board_id','category','title','content','tags','bet_points','attached_image')

        latest_search_word = set(SearchHistory.objects.values_list('search_word',flat=True).reverse()[0:8])

        related_room_list = RoomJoining.objects.filter(user_id = request.user.user_id)


        context = {
            'board_list':board_list,
            'recommend_board_list':recommend_board_list,
            'latest_board_list':latest_board_list,
            'latest_search_word':latest_search_word,
            'related_room_list':related_room_list,
        }

        return render(request,'top-page_board.html',context)

    def post(self,request,*args,**kwargs):

        if request.GET:
            search_terms = request.GET

        else:
            search_terms = request.POST
            search_history = SearchHistory(search_user_id=request.user.user_id,search_word=search_terms['search_word'])
            search_history.save()


        if search_terms['filtering_department'] == '全て':
            search_result = Boards.objects.filter(Q(title__istartswith=search_terms['search_word'])|Q(tags__istartswith=search_terms['search_word'])).values().order_by('created_at').reverse()
            if search_terms['selection_style_board'] == '全て':
                search_result = Boards.objects.filter(Q(title__istartswith=search_terms['search_word'])|Q(tags__istartswith=search_terms['search_word'])).values().order_by('created_at').reverse()

            else:
                search_result = Boards.objects.filter(Q(title__istartswith=search_terms['search_word'])|Q(tags__istartswith=search_terms['search_word']),category=search_terms['selection_style_board']).values().order_by('created_at').reverse()


        else:
            search_result = Boards.objects.filter(Q(title__istartswith=search_terms['search_word'])|Q(tags__istartswith=search_terms['search_word']),related_department=search_terms['filtering_department']).values().order_by('created_at').reverse()

            if search_terms['selection_style_board'] == '全て':
                search_result = Boards.objects.filter(Q(title__istartswith=search_terms['search_word'])|Q(tags__istartswith=search_terms['search_word']),related_department=search_terms['filtering_department']).values().order_by('created_at').reverse()

            else:
                search_result = Boards.objects.filter(Q(title__istartswith=search_terms['search_word'])|Q(tags__istartswith=search_terms['search_word']),related_department=search_terms['filtering_department'],category=search_terms['selection_style_board']).values().order_by('created_at').reverse()

        try:
            base_user = request.user.user_id
            random_extracting_user = Users.objects.filter(university = request.user.university).exclude(user_id=request.user.user_id).order_by('?')[:30].values_list('user_id',flat=True)
            recommend_board_list = recommend_system.get_recommend_board_main(base_user,random_extracting_user)

        except:
            recommend_board_list = Boards.objects.filter(university=request.user.university)[0:8]

        context = {
            'search_result_board_list':search_result,
            'recommend_board_list':recommend_board_list,
        }

        return render(request,'board_search_result.html',context)

top_page_board = TopPageBoardView.as_view()

@login_required
def preview_board_image(request):
    return JsonResponse()


class BoardView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        add_history = BrowsingHistory(user_id = request.user.user_id,board_id = self.kwargs['board_id'])
        add_history.save()


        try:
            base_user = request.user.user_id
            random_extracting_user = Users.objects.filter(university = request.user.university).exclude(user_id=request.user.user_id).order_by('?')[:30].values_list('user_id',flat=True)
            recommend_board_list = recommend_system.get_recommend_board_sub(base_user,random_extracting_user)

        except:
            recommend_board_list = Boards.objects.filter(university=request.user.university)[0:8]

        board_content = Boards.objects.get(board_id = self.kwargs['board_id'])
        board_post_user_data = Users.objects.get(user_id = board_content.posted_by_id)
        board_comment_list = BoardComment.objects.filter(comment_board_id = self.kwargs['board_id']).values().order_by('created_at').reverse()

        board_views = BrowsingHistory.objects.filter(board_id = self.kwargs['board_id']).count()

        good_board_id_list = GoodBoard.objects.filter(good_user_id = request.user.user_id).values_list('board_id',flat=True)
        store_board_id_list = StoreBoard.objects.filter(store_user_id = request.user.user_id).values_list('board_id',flat=True)

        context = {
            'board_content':board_content,
            'board_post_user_data':board_post_user_data,
            'recommend_board_list':recommend_board_list,
            'board_comment_list':list(board_comment_list),
            'board_views':board_views,
            'good_board_id_list':good_board_id_list,
            'store_board_id_list':store_board_id_list,
        }

        return render(request,'board.html',context)

    def post(self,request,*args,**kwargs):
        return HttpResponse('')

def search_board(requset):
    return HttpRespons('')

board = BoardView.as_view()


@login_required
def post_board(request):
    if request.method == 'POST':
        new_board_data = request.POST

        if int(new_board_data['bet_points']) < 0:
            return redirect('board:top_page_board')

        if(int(Users.objects.get(user_id=request.user.user_id).points) < int(new_board_data['bet_points']) and (new_board_data['category'] == '質問')):
            return redirect('board:top_page_board')

        elif int(Users.objects.get(user_id=request.user.user_id).points) > int(new_board_data['bet_points']) and (new_board_data['category'] == '質問'):
            consume_points_user = Users.objects.get(user_id = request.user.user_id)
            consume_points_user.points = int(consume_points_user.points) - int(new_board_data['bet_points'])
            consume_points_user.save()

        if int(new_board_data['bet_points']) != 0 and (new_board_data['category'] == '質問'):
            record_consume_points = PointsHistory(is_consumption=True,consumed_user_id=request.user.user_id,consumed_points=int(new_board_data['bet_points']),detail='ポイントを使って質問しました')
            record_consume_points.save()

        new_board_data_image_file = request.FILES

        try:
            if new_board_data_image_file['attached_image']:
                pass
        except:
            new_board_data_image_file['attached_image'] = ''

        try:
            if new_board_data_image_file['attached_file']:
                pass
        except:
            new_board_data_image_file['attached_file'] = ''


        create_board_data = Boards(category = new_board_data['category'],
                                    title = new_board_data['title'],
                                    content = new_board_data['content'],
                                    tags = new_board_data['tags'],
                                    related_department = new_board_data['related_department'],
                                    related_room_id = new_board_data['related_room'],
                                    bet_points = new_board_data['bet_points'],
                                    display_name = new_board_data['select_post_user'],
                                    posted_by_id = request.user.user_id,
                                    attached_image = new_board_data_image_file['attached_image'],
                                    attached_file = new_board_data_image_file['attached_file'],
                                    university = request.user.university)

        create_board_data.save()

        if new_board_data['related_room']:
            update_room = Rooms.objects.get(room_id = new_board_data['related_room'])
            update_room.last_update = timezone.now()
            update_room.save()

            display_name = Rooms.objects.get(room_id = new_board_data['related_room'])
            joining_room_id_list = RoomJoining.objects.filter(room_id = new_board_data['related_room']).exclude(user_id = request.user.user_id).values_list('user_id',flat=True)
            notification_list = []
            for notification in list(joining_room_id_list):
                add_notification = Notification(receiver_id=notification,room_id = new_board_data['related_room'],detail=new_board_data['title'],type='related_board',display_name=f'{display_name.room_name}')
                notification_list.append(add_notification)
            Notification.objects.bulk_create(notification_list)

        redirect_board_id = Boards.objects.get(posted_by_id=request.user.user_id,title = new_board_data['title'],content = new_board_data['content'],bet_points = new_board_data['bet_points']).board_id

        if new_board_data['category'] == '記事':
            add_purchase_data = PurchaseHistory(purchase_user_id=request.user.user_id,purchase_board_id=redirect_board_id)
            add_purchase_data.save()

            return redirect('board:confirm_view_board',board_id = redirect_board_id)

        else:
            return redirect('board:board',board_id = redirect_board_id)


    return redirect('board:board',board_id=redirect_board_id)


@login_required
def reply_comment(request):
    if request.method == 'POST':
        comment = request.POST
        image_file = request.FILES

        try:
            if image_file['comment_image']:
                pass
        except:
            image_file['comment_image']  = ''

        try:
            if image_file['comment_file']:
                pass
        except:
            image_file['comment_file']  = ''

        store_comment = BoardComment(comment_board_id=comment['board_id'],
                                        comment=comment['comment'],
                                        comment_user_id=request.user.user_id,
                                        comment_image=image_file['comment_image'],
                                        comment_file=image_file['comment_file'],
                                        display_name=comment['select_comment_user'],
                                        comment_nickname=f'{request.user.last_name}{request.user.first_name}'
                                        )
        store_comment.save()

        if comment['board_category'] == '記事':
            return redirect('board:confirm_view_board',board_id=comment['board_id'])
        else:
            return redirect('board:board',board_id=comment['board_id'])


@login_required
def evaluation(request):
    if request.method == 'GET':
        evaluation = request.GET
        evaluation_board = Boards.objects.get(board_id = evaluation['board_id'])
        evaluation_board.best_board = True
        evaluation_board.save()

        evaluation_comment = BoardComment.objects.get(comment_id = evaluation['comment_id'])
        evaluation_comment.best_board = True
        evaluation_comment.save()

        give_point_user = Users.objects.get(user_id = evaluation['evaluation_user_id'])
        give_point_user.points = int(give_point_user.points) + int(evaluation['bet_points'])
        give_point_user.save()

        if int(evaluation['bet_points']) > 0:
            record_consume_points = PointsHistory(is_consumption=True,consumed_points=int(evaluation['bet_points']),consumed_user_id=request.user.user_id,detail='ベストリプライに選出されました')
            record_consume_points.save()

        return HttpResponse('')


@login_required
def confirm_view_board(request,board_id):
    if request.method == 'GET':
        try:
            purchase_data = PurchaseHistory.objects.get(purchase_user_id=request.user.user_id,purchase_board_id=board_id)

        except:
            add_purchase_data = PurchaseHistory(purchase_user_id=request.user.user_id,purchase_board_id=board_id)
            add_purchase_data.save()


            board_point = Boards.objects.get(board_id = board_id).bet_points

            pay_point = Users.objects.get(user_id=request.user.user_id)

            if 0 > int(pay_point.points) - int(board_point):
                return redirect('board:top_page_board')

            pay_point.points = int(pay_point.points) - int(board_point)


            board_owner_id = Boards.objects.get(board_id = board_id).posted_by_id
            get_point = Users.objects.get(user_id = board_owner_id)
            get_point.points = int(get_point.points) + int(board_point)


            pay_point.save()
            get_point.save()

            record_get_points = PointsHistory(is_consumption=False,consumed_points=board_point,consumed_user_id=board_owner_id,detail='投稿した記事が閲覧されました')
            record_get_points.save()

            if int(board_point) > 0:
                record_consume_points = PointsHistory(is_consumption=True,consumed_points=board_point,consumed_user_id=request.user.user_id,detail='ポイントを使って記事を閲覧しました')
                record_consume_points.save()

            purchase_data = PurchaseHistory.objects.get(purchase_user_id = request.user.user_id,purchase_board_id=board_id)


        add_history = BrowsingHistory(user_id = request.user.user_id,board_id = board_id)
        add_history.save()

        base_user = request.user.user_id
        random_extracting_user = Users.objects.filter(university = request.user.university).exclude(user_id=request.user.user_id).order_by('?')[:30].values_list('user_id',flat=True)
        recommend_board_list = recommend_system.get_recommend_board_sub(base_user,random_extracting_user)

        board_content = Boards.objects.get(board_id = board_id)
        board_post_user_data = Users.objects.get(user_id = board_content.posted_by_id)
        board_comment_list = BoardComment.objects.filter(comment_board_id = board_id).values()

        board_views = BrowsingHistory.objects.filter(board_id = board_id).count()


        good_board_id_list = GoodBoard.objects.filter(good_user_id = request.user.user_id).values_list('board_id',flat=True)
        store_board_id_list = StoreBoard.objects.filter(store_user_id = request.user.user_id).values_list('board_id',flat=True)

        context = {
            'board_content':board_content,
            'board_post_user_data':board_post_user_data,
            'recommend_board_list':recommend_board_list,
            'board_comment_list':list(board_comment_list),
            'board_views':board_views,
            'purchase_data':purchase_data,
            'good_board_id_list':good_board_id_list,
            'store_board_id_list':store_board_id_list,
        }

        return render(request,'board.html',context)

@login_required
def good_board(request):
    if request.method == 'GET':
        if request.GET['state'] == 'non_executed':
            good_board = GoodBoard(board_id = request.GET['board_id'],good_user_id = request.user.user_id)
            good_board.save()

        elif request.GET['state'] == 'executed':
            delete_good_board = GoodBoard.objects.get(board_id=request.GET['board_id'],good_user_id = request.user.user_id)
            delete_good_board.delete()
        return HttpResponse('')

@login_required
def store_board(request):
    if request.method == 'GET':
        if request.GET['state'] == 'non_executed':
            store_board = StoreBoard(board_id = request.GET['board_id'],store_user_id = request.user.user_id)
            store_board.save()

        elif request.GET['state'] == 'executed':
            delete_store_board = StoreBoard.objects.get(board_id=request.GET['board_id'],store_user_id = request.user.user_id)
            delete_store_board.delete()
        return HttpResponse('')
