import os
from datetime import date

import streamlit as st
from supabase import create_client


# =========================================================
# APP CONFIG
# =========================================================

st.set_page_config(
    page_title="Event Business Manager",
    page_icon="🎪",
    layout="wide",
)


# =========================================================
# SUPABASE
# =========================================================

def get_secret(name):
    try:
        return st.secrets[name]
    except Exception:
        return os.getenv(name, "")


SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase secrets are missing.")
    st.stop()

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
)


# =========================================================
# HEADER
# =========================================================

st.title("🎪 Event Business Manager")
st.caption(
    "Events • Locations • Workers • Samaan"
)


# =========================================================
# TABS
# =========================================================

(
    dashboard_tab,
    events_tab,
    locations_tab,
    workers_tab,
    master_tab,
) = st.tabs(
    [
        "🏠 Dashboard",
        "🎪 Events",
        "📍 Locations",
        "👷 Workers",
        "📦 Samaan Master",
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

with dashboard_tab:

    st.subheader("🏠 Dashboard")

    try:

        events_result = (
            supabase
            .table("events")
            .select("id", count="exact")
            .execute()
        )

        locations_result = (
            supabase
            .table("locations")
            .select("id", count="exact")
            .eq("active", True)
            .execute()
        )

        workers_result = (
            supabase
            .table("workers")
            .select("id", count="exact")
            .eq("active", True)
            .execute()
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Events",
            events_result.count or 0,
        )

        col2.metric(
            "Locations",
            locations_result.count or 0,
        )

        col3.metric(
            "Workers",
            workers_result.count or 0,
        )

        st.success(
            "☁️ Supabase connected successfully."
        )

    except Exception as e:

        st.error(
            f"Dashboard error: {e}"
        )


# =========================================================
# EVENTS
# =========================================================

with events_tab:

    st.subheader("🎪 Events")

    # -----------------------------------------------------
    # CREATE EVENT
    # -----------------------------------------------------

    with st.expander(
        "➕ Create New Event",
        expanded=True,
    ):

        with st.form("create_event_form"):

            event_name = st.text_input(
                "Event Name *"
            )

            client_name = st.text_input(
                "Client Name"
            )

            event_date = st.date_input(
                "Event Date",
                value=date.today(),
            )

            create_event = st.form_submit_button(
                "Create Event"
            )

            if create_event:

                if not event_name.strip():

                    st.error(
                        "Event name is required."
                    )

                else:

                    try:

                        supabase.table(
                            "events"
                        ).insert(
                            {
                                "name":
                                    event_name.strip(),
                                "client_name":
                                    client_name.strip()
                                    or None,
                                "start_date":
                                    str(event_date),
                                "status":
                                    "upcoming",
                            }
                        ).execute()

                        st.success(
                            "Event created successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Could not create event: {e}"
                        )

    st.markdown("### 📋 Event List")

    try:

        events = (
            supabase
            .table("events")
            .select("*")
            .order("start_date")
            .execute()
        )

        if not events.data:

            st.info(
                "No events found."
            )

        for event in events.data:

            with st.expander(
                f"🎪 {event['name']} "
                f" — {event.get('start_date', '-')}"
            ):

                st.write(
                    f"**Client:** "
                    f"{event.get('client_name') or '-'}"
                )

                st.write(
                    f"**Status:** "
                    f"{event.get('status') or '-'}"
                )

    except Exception as e:

        st.error(
            f"Could not load events: {e}"
        )


# =========================================================
# LOCATIONS
# =========================================================

with locations_tab:

    st.subheader("📍 Locations")

    with st.expander(
        "➕ Add Location",
        expanded=True,
    ):

        with st.form("add_location_form"):

            location_name = st.text_input(
                "Location Name *"
            )

            address = st.text_area(
                "Address"
            )

            maps_link = st.text_input(
                "Google Maps Link"
            )

            add_location = st.form_submit_button(
                "Add Location"
            )

            if add_location:

                if not location_name.strip():

                    st.error(
                        "Location name is required."
                    )

                else:

                    try:

                        supabase.table(
                            "locations"
                        ).insert(
                            {
                                "name":
                                    location_name.strip(),
                                "location_type":
                                    "event",
                                "address":
                                    address.strip()
                                    or None,
                                "maps_link":
                                    maps_link.strip()
                                    or None,
                                "active":
                                    True,
                            }
                        ).execute()

                        st.success(
                            "Location added successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Could not add location: {e}"
                        )

    st.markdown("### 📋 Location List")

    try:

        locations = (
            supabase
            .table("locations")
            .select("*")
            .eq("active", True)
            .order("name")
            .execute()
        )

        if not locations.data:

            st.info(
                "No locations found."
            )

        for location in locations.data:

            with st.expander(
                f"📍 {location['name']}"
            ):

                st.write(
                    f"**Address:** "
                    f"{location.get('address') or '-'}"
                )

                if location.get("maps_link"):

                    st.markdown(
                        f"[🗺️ Open Google Maps]"
                        f"({location['maps_link']})"
                    )

    except Exception as e:

        st.error(
            f"Could not load locations: {e}"
        )


# =========================================================
# WORKERS
# =========================================================

with workers_tab:

    st.subheader("👷 Workers")

    with st.expander(
        "➕ Add Worker",
        expanded=True,
    ):

        with st.form("add_worker_form"):

            worker_name = st.text_input(
                "Worker Name *"
            )

            worker_phone = st.text_input(
                "Mobile"
            )

            add_worker = st.form_submit_button(
                "Add Worker"
            )

            if add_worker:

                if not worker_name.strip():

                    st.error(
                        "Worker name is required."
                    )

                else:

                    try:

                        supabase.table(
                            "workers"
                        ).insert(
                            {
                                "name":
                                    worker_name.strip(),
                                "phone":
                                    worker_phone.strip()
                                    or None,
                                "wage_type":
                                    "daily",
                                "wage_amount":
                                    0,
                                "active":
                                    True,
                            }
                        ).execute()

                        st.success(
                            "Worker added successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Could not add worker: {e}"
                        )

    st.markdown("### 📋 Worker List")

    try:

        workers = (
            supabase
            .table("workers")
            .select("id,name,phone,active")
            .eq("active", True)
            .order("name")
            .execute()
        )

        if not workers.data:

            st.info(
                "No workers found."
            )

        for worker in workers.data:

            col1, col2 = st.columns(
                [4, 2]
            )

            col1.write(
                f"👷 **{worker['name']}**"
            )

            col2.write(
                worker.get("phone")
                or "-"
            )

    except Exception as e:

        st.error(
            f"Could not load workers: {e}"
        )


# =========================================================
# SAMAAN MASTER
# =========================================================

with master_tab:

    st.subheader("📦 Samaan Master")

    st.caption(
        "Samaan ek baar add karo. "
        "Har event mein dobara naam nahi likhna padega."
    )

    # -----------------------------------------------------
    # ADD CATEGORY
    # -----------------------------------------------------

    with st.expander(
        "➕ Add Category",
        expanded=True,
    ):

        with st.form("add_category_form"):

            category_name = st.text_input(
                "Category Name"
            )

            add_category = st.form_submit_button(
                "Add Category"
            )

            if add_category:

                if not category_name.strip():

                    st.error(
                        "Category name required."
                    )

                else:

                    try:

                        supabase.table(
                            "item_categories"
                        ).insert(
                            {
                                "name":
                                    category_name.strip(),
                                "active":
                                    True,
                                "sort_order":
                                    0,
                            }
                        ).execute()

                        st.success(
                            "Category added."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Could not add category: {e}"
                        )

    # -----------------------------------------------------
    # CATEGORY LIST
    # -----------------------------------------------------

    try:

        categories = (
            supabase
            .table("item_categories")
            .select("*")
            .eq("active", True)
            .order("sort_order")
            .order("name")
            .execute()
        )

    except Exception as e:

        st.error(
            f"Could not load categories: {e}"
        )

        categories = None

    for category in (
        categories.data
        if categories
        else []
    ):

        with st.expander(
            f"📁 {category['name']}"
        ):

            with st.form(
                f"add_item_{category['id']}"
            ):

                item_name = st.text_input(
                    "Item Name"
                )

                add_item = st.form_submit_button(
                    "Add Item"
                )

                if add_item:

                    if not item_name.strip():

                        st.error(
                            "Item name required."
                        )

                    else:

                        try:

                            supabase.table(
                                "master_items"
                            ).insert(
                                {
                                    "category_id":
                                        category["id"],
                                    "item_name":
                                        item_name.strip(),
                                    "active":
                                        True,
                                    "sort_order":
                                        0,
                                }
                            ).execute()

                            st.success(
                                "Item added."
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Could not add item: {e}"
                            )

            try:

                items = (
                    supabase
                    .table("master_items")
                    .select("*")
                    .eq(
                        "category_id",
                        category["id"],
                    )
                    .eq("active", True)
                    .order("sort_order")
                    .order("item_name")
                    .execute()
                )

                if not items.data:

                    st.info(
                        "No items in this category."
                    )

                else:

                    for item in items.data:

                        st.write(
                            f"📦 {item['item_name']}"
                        )

            except Exception as e:

                st.error(
                    f"Could not load items: {e}"
                        )
