from django.shortcuts import render
from django.db.models import Prefetch
from taxi.models import Driver, Car, Manufacturer
from django.views.generic import ListView, DetailView


def index(request):
    """View function for the home page of the site."""
    context = {
        "num_drivers": Driver.objects.count(),
        "num_cars": Car.objects.count(),
        "num_manufacturers": Manufacturer.objects.count(),
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(ListView):
    model = Manufacturer
    queryset = Manufacturer.objects.all().order_by("name")
    paginate_by = 5


class CarListView(ListView):
    model = Car
    paginate_by = 5

    def get_queryset(self):
        return Car.objects.select_related("manufacturer")


class CarDetailView(DetailView):
    model = Car


class DriverListView(ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(DetailView):
    model = Driver

    def get_queryset(self):
        return Driver.objects.prefetch_related(
            Prefetch("cars",
                     queryset=Car.objects.select_related("manufacturer"))
        )
