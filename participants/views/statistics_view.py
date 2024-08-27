'''
MVP demo ver 0.0.8
2024.08.28
participants/views/statistics_view.py

역할: Django Rest Framework(DRF)를 사용하여 참가자의 개인 통계 API 엔드포인트의 로직을 처리
- 전체 통계, 연도별 통계, 기간별 통계
'''
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from participants.models import Participant
from participants.utils.statistics import calculate_statistics

from datetime import timedelta

from utils.error_handlers import handle_400_bad_request

class StatisticsViewSet(viewsets.ViewSet):
    '''
    참가자 개인 통계 클래스
    '''
    permission_classes = [IsAuthenticated]

    def list(self, request):
        '''
        사용 가능한 통계 API의 목록을 반환
        '''
        return Response({
            "status": status.HTTP_200_OK,
            "message": "Statistics API root",
            "data": {
                "endpoints": {
                    "overall": "GET /participants/statistics/overall/",
                    "yearly": "GET /participants/statistics/yearly/{year}/",
                    "period": "GET /participants/statistics/period/?start_date={start_date}&end_date={end_date}",
                    "ranks": "GET /clubs/statistics/ranks/?club_id={club_id}",
                    "events": "GET /clubs/statistics/events/?club_id={club_id}",
                }
            }
        })

    @action(detail=False, methods=['get'], url_path='overall')
    def overall_statistics(self, request):
        '''
        전체 통계
        GET /participants/statistics/overall/
        '''
        user = request.user  # 요청을 보낸 사용자를 가져옴
        participants = Participant.objects.filter(club_member__user=user)  # 해당 사용자의 모든 참가 데이터

        data = calculate_statistics(participants)

        return Response({
            "status": status.HTTP_200_OK,
            "message": "Successfully retrieved overall statistics",
            "data": data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='yearly/(?P<year>[0-9]{4})') # 0~9까지 4자리 수
    def yearly_statistics(self, request, year=None):
        '''
        연도별 통계 조회
        GET /participants/statistics/yearly/{year}/
        '''
        user = request.user
        participants = Participant.objects.filter(club_member__user=user,
                                                  event__start_date_time__year=year)  # 특정 연도의 참가 데이터

        data = calculate_statistics(participants, year=year)

        return Response({
            "status": status.HTTP_200_OK,
            "message": f"Successfully retrieved statistics for the year {year}",
            "data": data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='period')
    def period_statistics(self, request):
        '''
        기간별 통계 조회
        GET /participants/statistics/period/?start_date={start_date}&end_date={end_date}
        '''
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:  # 날짜가 제공되지 않은 경우 400
            return handle_400_bad_request("start_date and end_date query parameters are required.")

        # 날짜를 datetime 객체로 변환
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # end_date를 다음 날로 설정하여 해당 날짜의 끝까지 포함
        end_date = end_date + timedelta(days=1) - timedelta(seconds=1)

        user = request.user
        participants = Participant.objects.filter( # 특정 날짜 범위 내의 참가 데이터
            club_member__user=user,
            event__start_date_time__range=[start_date, end_date + timedelta(days=1)] # 범위 지정할 때에 2번째 인자는 미만으로 처리되므로 end_date에 +1
        )

        data = calculate_statistics(participants, start_date=start_date, end_date=end_date)
        return Response({
            "status": status.HTTP_200_OK,
            "message": f"Successfully retrieved statistics for the period {start_date} to {end_date}",
            "data": data
        }, status=status.HTTP_200_OK)