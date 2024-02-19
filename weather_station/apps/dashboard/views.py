from django.views import View
from django.shortcuts import render
from django.utils import timezone

import plotly.express as px

from apps.sensor.models import IndoorSensorData


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        filter_option = request.GET.get("filter_option", "all")
        sensor_data = self.get_filtered_sensor_data(filter_option)

        x_data = [data.created for data in sensor_data]
        temperature_data = [data.temperature for data in sensor_data]
        humidity_data = [data.humidity for data in sensor_data]
        pressure_data = [data.pressure for data in sensor_data]
        co2_data = [data.co2 for data in sensor_data]

        fig = px.line(
            x=x_data,
            y=[temperature_data, humidity_data, pressure_data, co2_data],
            title="Sensor Daten",
            labels={"x": "Zeit", "y": "Sensordaten"},
        )

        fig.update_layout(title={"font_size": 22, "xanchor": "center", "x": 0.5})

        chart = fig.to_html()

        context = {"chart": chart}

        return render(request, self.template_name, context)

    def get_filtered_sensor_data(self, filter_option):
        now = timezone.now()

        if filter_option == "day":
            return IndoorSensorData.objects.filter(created__date=now.date())

        elif filter_option == "week":
            start_of_week = now - timezone.timedelta(days=now.weekday())
            end_of_week = start_of_week + timezone.timedelta(days=6)
            return IndoorSensorData.objects.filter(
                created__date__range=[start_of_week.date(), end_of_week.date()]
            )

        elif filter_option == "month":
            return IndoorSensorData.objects.filter(
                created__year=now.year, created__month=now.month
            )

        elif filter_option == "year":
            return IndoorSensorData.objects.filter(created__year=now.year)

        else:
            return IndoorSensorData.objects.all()
