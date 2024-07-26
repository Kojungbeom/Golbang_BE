from datetime import datetime

from .models import Event


class EventUtils:
    # 해당 달의 이벤트 리스트를 가져오는 쿼리
    @staticmethod
    def get_month_events_queryset(year, month, status_type, user):

        start_date = datetime(year, month, 1)
        next_month = month % 12 + 1
        next_month_year = year if month < 12 else year + 1
        end_date = datetime(next_month_year, next_month, 1)

        events = (Event.objects
                  .filter(participant__member__user=user,
                          start_date_time__gte=start_date,
                          start_date_time__lt=end_date)
                  .order_by('start_date_time'))

        if status_type is None:
            return events

        return events.filter(participant__status_type__in=['ACCEPT', 'PARTY'])
