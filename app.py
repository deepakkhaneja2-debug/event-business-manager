```python
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

try:
    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY,
    )
except Exception as e:
    st.error(f"Supabase connection failed: {e}")
    st.stop()


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

        categories_result = (
            supabase
            .table("item_categories")
            .select("id", count="exact")
            .eq("active", True)
            .execute()
        )

        col1, col2, col3, col4 = st.columns(4)

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

        col4.metric(
            "Samaan Categories",
            categories_result.count or 0,
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

            event_type = st.text_input(
                "Event Type"
            )

            venue = st.text_input(
                "Venue / Location"
            )

            col1, col2 = st.columns(2)

            with col1:

                start_date = st.date_input(
                    "Start Date",
                    value=date.today(),
                )

            with col2:

                end_date = st.date_input(
                    "End Date",
                    value=date.today(),
                )

            col3, col4 = st.columns(2)

            with col3:

                total_amount = st.number_input(
                    "Total Amount",
                    min_value=0.0,
                    step=1000.0,
                )

            with col4:

                advance_received = st.number_input(
                    "Advance Received",
                    min_value=0.0,
                    step=1000.0,
                )

            notes = st.text_area(
                "Notes"
            )

            col5, col6 = st.columns(2)

            with col5:

                show_location = st.toggle(
                    "📍 Show Location to Workers",
                    value=False,
                )

            with col6:

                show_items = st.toggle(
                    "📦 Show Samaan to Workers",
                    value=True,
                )

            create_event = st.form_submit_button(
                "➕ Create Event"
            )

            if create_event:

                if not event_name.strip():

                    st.error(
                        "Event name is required."
                    )

                elif end_date < start_date:

                    st.error(
                        "End Date cannot be before Start Date."
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

                                "venue":
                                    venue.strip()
                                    or None,

                                "start_date":
                                    str(start_date),

                                "end_date":
                                    str(end_date),

                                "event_type":
                                    event_type.strip()
                                    or None,

                                "total_amount":
                                    total_amount,

                                "advance_received":
                                    advance_received,

                                "status":
                                    "upcoming",

                                "notes":
                                    notes.strip()
                                    or None,

                                "show_location_to_workers":
                                    show_location,

                                "show_items_to_workers":
                                    show_items,
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

    # -----------------------------------------------------
    # EVENT LIST
    # -----------------------------------------------------

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

        else:

            for event in events.data:

                with st.expander(
                    f"🎪 {event.get('name', '-')}"
                    f" — {event.get('start_date', '-')}"
                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"**Client:** "
                            f"{event.get('client_name') or '-'}"
                        )

                        st.write(
                            f"**Event Type:** "
                            f"{event.get('event_type') or '-'}"
                        )

                        st.write(
                            f"**Venue:** "
                            f"{event.get('venue') or '-'}"
                        )

                        st.write(
                            f"**Start:** "
                            f"{event.get('start_date') or '-'}"
                        )

                        st.write(
                            f"**End:** "
                            f"{event.get('end_date') or '-'}"
                        )

                    with col2:

                        st.write(
                            f"**Status:** "
                            f"{event.get('status') or '-'}"
                        )

                        st.write(
                            f"**Total:** "
                            f"₹{event.get('total_amount') or 0}"
                        )

                        st.write(
                            f"**Advance:** "
                            f"₹{event.get('advance_received') or 0}"
                        )

                        location_status = (
                            "🟢 ON"
                            if event.get(
                                "show_location_to_workers"
                            )
                            else "🔴 OFF"
                        )

                        item_status = (
                            "🟢 ON"
                            if event.get(
                                "show_items_to_workers"
                            )
                            else "🔴 OFF"
                        )

                        st.write(
                            f"📍 Location: "
                            f"{location_status}"
                        )

                        st.write(
                            f"📦 Samaan: "
                            f"{item_status}"
                        )

                    if event.get("notes"):

                        st.info(
                            f"📝 {event['notes']}"
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

            location_type = st.selectbox(
                "Location Type",
                [
                    "event",
                    "venue",
                    "other",
                ],
            )

            landlord_name = st.text_input(
                "Contact / Owner Name"
            )

            landlord_phone = st.text_input(
                "Contact / Owner Mobile"
            )

            add_location = st.form_submit_button(
                "➕ Add Location"
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
                                    location_type,

                                "address":
                                    address.strip()
                                    or None,

                                "maps_link":
                                    maps_link.strip()
                                    or None,

                                "landlord_name":
                                    landlord_name.strip()
                                    or None,

                                "landlord_phone":
                                    landlord_phone.strip()
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

        else:

            for location in locations.data:

                with st.expander(
                    f"📍 {location['name']}"
                ):

                    st.write(
                        f"**Type:** "
                        f"{location.get('location_type') or '-'}"
                    )

                    st.write(
                        f"**Address:** "
                        f"{location.get('address') or '-'}"
                    )

                    if location.get(
                        "landlord_name"
                    ):

                        st.write(
                            f"**Contact:** "
                            f"{location['landlord_name']}"
                        )

                    if location.get(
                        "landlord_phone"
                    ):

                        st.write(
                            f"**Mobile:** "
                            f"{location['landlord_phone']}"
                        )

                    if location.get(
                        "maps_link"
                    ):

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

            wage_type = st.selectbox(
                "Wage Type",
                [
                    "daily",
                    "monthly",
                ],
            )

            wage_amount = st.number_input(
                "Wage / Salary",
                min_value=0.0,
                step=100.0,
            )

            joining_date = st.date_input(
                "Joining Date",
                value=date.today(),
            )

            add_worker = st.form_submit_button(
                "➕ Add Worker"
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
                                    wage_type,

                                "wage_amount":
                                    wage_amount,

                                "joining_date":
                                    str(joining_date),

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
            .select("*")
            .eq("active", True)
            .order("name")
            .execute()
        )

        if not workers.data:

            st.info(
                "No workers found."
            )

        else:

            for worker in workers.data:

                col1, col2, col3 = st.columns(
                    [4, 2, 2]
                )

                col1.write(
                    f"👷 **{worker['name']}**"
                )

                col2.write(
                    worker.get("phone")
                    or "-"
                )

                wage_type_display = (
                    worker.get("wage_type")
                    or "-"
                ).title()

                col3.write(
                    f"{wage_type_display}: "
                    f"₹{worker.get('wage_amount') or 0}"
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
        "Samaan ek baar yahan add karo. "
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
                "➕ Add Category"
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

                                "active": True, "sort_order": 0, } ).execute() st.success( "Category added." ) st.rerun() except Exception as e: st.error( f"Could not add category: {e}" ) # ----------------------------------------------------- # CATEGORY LIST # ----------------------------------------------------- try: categories = ( supabase .table("item_categories") .select("*") .eq("active", True) .order("sort_order") .order("name") .execute() ) category_data = ( categories.data or [] ) except Exception as e: st.error( f"Could not load categories: {e}" ) category_data = [] for category in category_data: with st.expander( f"📁 {category['name']}" ): # --------------------------------------------- # ADD ITEM # --------------------------------------------- with st.form( f"add_item_{category['id']}" ): item_name = st.text_input( "Item Name" ) add_item = st.form_submit_button( "➕ Add Item" ) if add_item: if not item_name.strip(): st.error( "Item name required." ) else: try: supabase.table( "master_items" ).insert( { "category_id": category["id"], "item_name": item_name.strip(), "active": True, "sort_order": 0, } ).execute() st.success( "Item added." ) st.rerun() except Exception as e: st.error( f"Could not add item: {e}" ) # --------------------------------------------- # ITEMS # --------------------------------------------- try: items = ( supabase .table("master_items") .select("*") .eq( "category_id", category["id"], ) .eq("active", True) .order("sort_order") .order("item_name") .execute() ) item_data = ( items.data or [] ) except Exception as e: st.error( f"Could not load items: {e}" ) item_data = [] if not item_data: st.info( "No items in this category." ) else: for item in item_data: st.write( f"📦 {item['item_name']}" )