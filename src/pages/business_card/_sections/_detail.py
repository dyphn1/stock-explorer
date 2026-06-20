"""Business card section: detail sections (share, footer)."""
import streamlit as st
import urllib.parse
from src.pages._router_base import _info_card, _section_title
from src.core.i18n import t


def _render_share_section(data: dict, client) -> None:
    """C53-1: Social Sharing — shareable URL for this analysis card."""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    page = st.session_state.get("page", "名片")

    # Build shareable URL using current query_params as base
    params = urllib.parse.urlencode({"page": page, "stock_id": stock_id})
    # Use JavaScript-injected URL to get the full origin + path
    share_url_js = urllib.parse.quote(f"?{params}", safe="=?&")

    st.markdown("---")
    _section_title(t("detail:share_card"))

    # Use JS to get the full current URL (origin + path) and build shareable link
    js_get_url = """
    <script>
    (function() {
        var fullUrl = window.location.origin + window.location.pathname + '""" + f"?{params}" + """';
        var input = document.getElementById('share-url-input');
        if (input) {
            input.value = fullUrl;
        }
        // Also update the copy link
        var copyLink = document.getElementById('share-copy-btn');
        if (copyLink) {
            copyLink.href = fullUrl;

            // Expand the parent anchor to cover the icon area
            var p = copyLink.closest('p');
            if (p) {
                p.style.margin = '0';
                p.style.padding = '0';
                p.style.lineHeight = '1';
            }
        }
    })();
    </script>
    """

    col1, col2 = st.columns([5, 1])
    with col1:
        # Read-only text input with the shareable URL
        # Start with a placeholder; JS will update it with the full URL
        placeholder_params = f"?page={page}&stock_id={stock_id}"
        st.text_input(
            t("detail:share_link_label"),
            value=placeholder_params,
            label_visibility="collapsed",
            key=f"share_url_{stock_id}_{page}",
            help=t("detail:share_link_help"),
        )

    with col2:
        # Copy button using JS clipboard API
        copy_js = """
        <script>
        function copyShareUrl() {
            var params = '""" + f"?{params}" + """';
            var fullUrl = window.location.origin + window.location.pathname + params;
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(fullUrl).then(function() {
                    var btn = document.getElementById('share-copy-icon');
                    if (btn) {
                        btn.textContent = '✅';
                        setTimeout(function() { btn.textContent = '📋'; }, 2000);
                    }
                });
            } else {
                // Fallback: select the input text
                var input = document.getElementById('share-url-input');
                if (input) {
                    input.value = fullUrl;
                    input.select();
                    document.execCommand('copy');
                }
            }
        }
        </script>
        <a id="share-copy-btn" onclick="copyShareUrl(); return false;"
           style="cursor:pointer;text-decoration:none;font-size:1.4rem;
                  display:inline-block;padding:0.3rem 0.6rem;
                  background:#F8F9FA;border-radius:8px;
                  text-align:center;min-width:2.2rem;"
           title=t("detail:share_link_title")>
            <span id="share-copy-icon">📋</span>
        </a>
        """
        st.html(copy_js)

    st.html(js_get_url)


def _render_footer(data: dict, client) -> None:
    """Disclaimer."""
    st.markdown("---")

    # 免責聲明
    _info_card(t("detail:disclaimer_title"), t("detail:disclaimer_content"), "⚠️")
