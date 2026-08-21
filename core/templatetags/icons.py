"""
Inline SVG icon tag.

Renders small stroke icons directly in markup (no icon font, no JS library)
so they inherit colour via `currentColor` and resize with a Tailwind class.

Note: these are line-icon stand-ins for the exact icons exported in the
Figma file — this build environment has no network route to Figma's asset
CDN, so the real exports couldn't be pulled in. Swap the paths below for the
real exports whenever that's convenient; nothing else needs to change since
every call site just names an icon.
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# icon name -> inner SVG markup (24x24 viewBox, stroke-based)
_ICONS = {
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 4c0 2.1-.8 4.3-2 6h1.5c-.1 5-4 8-5.5 10z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "user": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "cart": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
    "chevron-down": '<polyline points="6 9 12 15 18 9"/>',
    "map-pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
    "arrow-right": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.8 1-1a5.5 5.5 0 0 0 0-7.8Z"/>',
    "plus": '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "truck": '<path d="M1 3h15v13H1z"/><path d="M16 8h4l3 3v5h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>',
    "droplet": '<path d="M12 2.7s6 6.5 6 10.7a6 6 0 0 1-12 0c0-4.2 6-10.7 6-10.7z"/>',
    "sparkles": '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3Z"/>',
}


@register.simple_tag
def icon(name, css_class="size-4"):
    """Usage: {% icon "search" "size-5 text-ink-muted" %}"""
    inner = _ICONS.get(name, "")
    return mark_safe(
        f'<svg class="{css_class}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'
    )
