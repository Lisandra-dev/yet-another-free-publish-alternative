---
layout: post
title: Notes
permalink: /feed/
content-type: eg
---
<style>
.container {
    padding-bottom: 0;
}
.scroll-to-top {
    display: none
}

</style>

{%- for item in site.documents reversed -%}
    {%- if item.flux != false-%}
        <div class="feed-title-excerpt-block disable-select" data-url="{{site.url}}{{item.url}}">
            <a href="{{ item.url }}" style="text-decoration: none; color: #555555;">
                <ul style="padding-left: 20px; margin-top: 20px;" class="tags">
                    <li style="padding: 0 5px; border-radius: 10px;" class="tag">{{item.date | date_to_string | capitalize }}</li>
                </ul>
                <p style="margin-top: 0px;" class="feed-title">{{ item.title }}</p>
                <p class="feed-excerpt">{{item.resume }}</p>
            </a>
        </div>
    {%- endif -%}
{%- endfor -%}
<br/>
<br/>
