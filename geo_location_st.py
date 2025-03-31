import streamlit as st
import streamlit.components.v1 as components

st.title("Get Current Location in Streamlit")

html_code = """
<script>
navigator.geolocation.getCurrentPosition((position) => {
    const coords = position.coords;
    document.getElementById("data").innerText = 
        `Latitude: ${coords.latitude}, Longitude: ${coords.longitude}`;
});
</script>
<div id="data">Fetching location...</div>
"""

components.html(html_code)
