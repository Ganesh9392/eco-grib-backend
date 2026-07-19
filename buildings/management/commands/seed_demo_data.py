import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from analytics.models import EnergyRecord
from buildings.models import Building, Fixture

User = get_user_model()


class Command(BaseCommand):
    help = "Creates sample buildings, fixtures, users and 30 days of energy records so the frontend has something to show."

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # --- Buildings -------------------------------------------------
        buildings_data = [
            {"name": "HQ Tower North", "address": "120 Market St", "city": "San Francisco", "floors": 18, "rooms": 220, "occupancy_rate": 0.72},
            {"name": "Innovation Campus", "address": "88 Innovation Way", "city": "Austin", "floors": 6, "rooms": 96, "occupancy_rate": 0.61},
            {"name": "West Distribution", "address": "500 Logistics Blvd", "city": "Denver", "floors": 3, "rooms": 42, "occupancy_rate": 0.44},
            {"name": "Downtown Office", "address": "310 Grand Ave", "city": "Chicago", "floors": 12, "rooms": 164, "occupancy_rate": 0.68},
        ]
        buildings = []
        for b in buildings_data:
            building, _ = Building.objects.update_or_create(name=b["name"], defaults=b)
            buildings.append(building)

        # --- Fixtures ----------------------------------------------------
        rooms = ["Office 101", "Meeting Room A", "Lobby", "Corridor 2", "Cafeteria"]
        for building in buildings:
            for i in range(1, 9):
                online = i % 5 != 0
                Fixture.objects.update_or_create(
                    name=f"{building.name[:3].upper()}-Fixture-{i}",
                    building=building,
                    defaults={
                        "room_name": rooms[i % len(rooms)],
                        "is_on": online and i % 3 != 0,
                        "brightness": random.randint(30, 100) if online else 0,
                        "power_w": round(random.uniform(10, 35), 1) if online else 0,
                        "voltage_v": round(random.uniform(220, 240), 1) if online else 0,
                        "current_a": round(random.uniform(0.1, 0.6), 2) if online else 0,
                        "operating_hours": random.randint(500, 9000),
                        "health": random.choice(["healthy", "healthy", "healthy", "warning", "critical"]),
                        "firmware": "v2.3.1",
                        "status": "online" if online else "offline",
                    },
                )

        # --- Users -------------------------------------------------
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@ecogrid.io", "admin12345", role="Admin")
            self.stdout.write("Created superuser: admin / admin12345")

        demo_users = [
            {"username": "elena.ruiz", "first_name": "Elena", "last_name": "Ruiz", "email": "elena@ecogrid.io", "role": "Manager", "building": buildings[0]},
            {"username": "priya.nair", "first_name": "Priya", "last_name": "Nair", "email": "priya@ecogrid.io", "role": "Operator", "building": buildings[3]},
            {"username": "sara.kim", "first_name": "Sara", "last_name": "Kim", "email": "sara.kim@ecogrid.io", "role": "Viewer", "building": buildings[1], "is_active": False},
        ]
        for u in demo_users:
            if not User.objects.filter(username=u["username"]).exists():
                user = User(**u)
                user.set_password("changeme123")
                user.save()

        # --- Energy records (last 30 days) -------------------------------
        today = timezone.now().date()
        for building in buildings:
            base = building.rooms * 15  # rough baseline load
            for day_offset in range(30):
                date = today - timedelta(days=day_offset)
                used = round(base + random.uniform(-200, 300), 2)
                saved = round(used * random.uniform(0.1, 0.22), 2)
                EnergyRecord.objects.update_or_create(
                    building=building,
                    date=date,
                    defaults={
                        "kwh_used": used,
                        "kwh_saved": saved,
                        "co2_reduced_kg": round(saved * 0.4, 2),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Done. Sample buildings, fixtures, users and energy records created."))
