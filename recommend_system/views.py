from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from accounts.models import Users
from .models import BrowsingHistory
from django.utils import timezone
from board.models import Boards
from collections import OrderedDict


@login_required
def recommend_board_at_main_page(request):

    '''ユーザーテーブルとブラウジング履歴テーブルを内部結合する'''

    #100人の同大学のユーザーを取得する
    base_user = request.user.user_id
    random_extracting_user = Users.objects.filter(university = request.user.university).exclude(user_id=request.user.user_id).order_by('?')[:30].values_list('user_id',flat=True)
    # random_extracting_browsing_history = BrowsingHistory.objects.all()





    return redirect('mypage:mypage',request.user.user_id)




def juccard(data1,data2):
    broad_match = set(data1) & set(data2)
    whole_set = set(data1)|set(data2)
    return (len(broad_match)/len(whole_set))








def get_recommend_board_sub(base_user,random_extracting_user):
    browsing_history_similarity = {}
    base_user_history = BrowsingHistory.objects.filter(user_id = base_user).values_list('board_id',flat=True)[:20]
    for random_user in random_extracting_user:
        random_user_history = BrowsingHistory.objects.filter(user_id=random_user).values_list('board_id',flat=True)[:20]

        browsing_history_similarity[random_user] = [juccard(list(base_user_history),list(random_user_history)),list(random_user_history)]

    sorted_browsing_history_similarity = dict(sorted(browsing_history_similarity.items()))

    recommend_board_id_score = {}
    recommend_board_id_list = []
    for key,value in sorted_browsing_history_similarity.items():
        difference_set = set(value[1]) - set(list(base_user_history))
        for recommend_board in difference_set:
            if(recommend_board in recommend_board_id_score.keys()):
                recommend_board_id_score[recommend_board] = recommend_board_id_score[recommend_board] +0.08
            else:
                recommend_board_id_score[recommend_board] = value[0]
                recommend_board_id_list.append(recommend_board)

    board_list = Boards.objects.filter(board_id__in = recommend_board_id_list).values()

    recommend_board_list = []
    for board_data in board_list:
        for board_id_score in recommend_board_id_score:
            if(board_data['board_id'] == board_id_score):
                board_data['recommend_points'] = recommend_board_id_score[board_id_score] + (board_data['bet_points'] / 10) - (((timezone.now() - board_data['created_at']).days)/40)
                recommend_board_list.append(board_data)

                break

    for i in range(len(recommend_board_list)):
        for j in range(i+1,len(recommend_board_list),1):
            if(recommend_board_list[i]['recommend_points'] < recommend_board_list[j]['recommend_points']):
                max = recommend_board_list[j]
                min = recommend_board_list[i]

                recommend_board_list[i] = max
                recommend_board_list[j] = min

    return recommend_board_list



def get_recommend_board_main(base_user,random_extracting_user):
    browsing_history_similarity = {}
    base_user_history = BrowsingHistory.objects.filter(user_id = base_user).values_list('board_id',flat=True)[:20]
    for random_user in random_extracting_user:
        random_user_history = BrowsingHistory.objects.filter(user_id=random_user).values_list('board_id',flat=True)[:20]

        browsing_history_similarity[random_user] = [juccard(list(base_user_history),list(random_user_history)),list(random_user_history)]

    sorted_browsing_history_similarity = dict(sorted(browsing_history_similarity.items()))

    recommend_board_id_score = {}
    recommend_board_id_list = []
    for key,value in sorted_browsing_history_similarity.items():
        difference_set = set(value[1]) - set(list(base_user_history))
        for recommend_board in difference_set:
            if(recommend_board in recommend_board_id_score.keys()):
                recommend_board_id_score[recommend_board] = recommend_board_id_score[recommend_board] +0.08
            else:
                recommend_board_id_score[recommend_board] = value[0]
                recommend_board_id_list.append(recommend_board)


    board_list = Boards.objects.filter(board_id__in = recommend_board_id_list).values()

    recommend_board_list = []
    for board_data in board_list:
        for board_id_score in recommend_board_id_score:
            if(board_data['board_id'] == board_id_score):
                board_data['recommend_points'] = recommend_board_id_score[board_id_score] + (board_data['bet_points'] / 6) - (((timezone.now() - board_data['created_at']).days)/65)
                recommend_board_list.append(board_data)

                break

    for i in range(len(recommend_board_list)):
        for j in range(i+1,len(recommend_board_list),1):
            if(recommend_board_list[i]['recommend_points'] < recommend_board_list[j]['recommend_points']):
                max = recommend_board_list[j]
                min = recommend_board_list[i]

                recommend_board_list[i] = max
                recommend_board_list[j] = min

    return recommend_board_list






def create_recommend_board_list(request):
    my_history = BrowsingHistory.objects.filter(user_id = request.user.user_id).values_list('board_id',flat=True)[:30]
    random_users = Users.objects.all().exclude(user_id = request.user.user_id).values_list('user_id',flat=True)[:30]

    random_user_board_list = []
    random_users_board_list = []

    for user in random_users:
        for _ in BrowsingHistory.objects.filter(user_id = user).values_list('board_id',flat=True)[:30]:
            random_user_board_list.append(_)
        random_users_board_list.append(random_user_board_list)
        random_user_board_list = []

    similar_board_list = {}
    for _1 in random_users_board_list:
        similar_board_list[juccard(my_history,_1)] = _1

    sorted_similar_board_list = sorted(similar_board_list.items(), key=lambda x:x[0],reverse=True)

    recommend_board_list = []
    for _2 in sorted_similar_board_list:
        for _3 in _2[1]:
            recommend_board_list.append(_3)

    sorted_recommend_board_list = list(OrderedDict.fromkeys(recommend_board_list))

    board_point = 0
    recommend_board_list = {}
    for _4 in sorted_recommend_board_list:
        if _4 in my_history:
            pass
        else:
            board = Boards.objects.get(board_id = _4)
            board_point = (board.bet_points + 1)*0.25
            board_point += 50/(((timezone.now() - board.created_at).days)+1)
            recommend_board_list[board.board_id] = board_point
            board_point = 0

    sorted_board_list = sorted(recommend_board_list.items(), key=lambda x:x[1],reverse=True)
    board_list = []
    for _5 in sorted_board_list:
        board_list.append(_5[0])

    return board_list
