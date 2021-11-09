---
layout: post
permalink: /collection/
content-type: eg
---

<style>
summary.cat {
	position: sticky;
	top: 0;
	background-color: white;
}
</style>

{%- if page.permalink == "/collection/"-%}
  {% for collection in site.collections %}
    {%- if collection.label != "private" and collection.label != "posts" -%}
        {%- assign docs = "/" | append: collection.label -%}
        <details class="first">
            <summary><a href="{{ docs }}">{{ collection.label | capitalize}}</a></summary>
                <ul>
                    {%- assign documents = site[collection.label] | group_by_exp: 'item', "item.category | downcase" -%}
                    {% for cat in documents %}
                        {%- if cat.name != 'false' -%}
                            <details class="second">
                                <summary class="cat">{{ cat.name | upcase }}</summary>
                                <ul>
                                {% assign items = cat.items | sort: 'date' | reverse %}
                                {% for item in items %}
                                    <div class="feed-title-excerpt-block disable-select" data-url="{{site.url}}{{item.url}}">
                                    <a href="{{ item.url }}" style="text-decoration: none; color: #555555;">
                                        <ul style="padding-left: 20px; margin-top: 20px;" class="tags">
                                            <li style="padding: 0 5px; border-radius: 10px;" class="tag">{{item.date | date_to_string | capitalize }}</li>
                                        </ul>
                                        <p style="margin-top: 0px;" class="feed-title">{{ item.title }}</p>
                                        <p class="feed-excerpt">{{item.description
                                            }}</p>
                                    </a>
                                </div>
                            {% endfor %}
                            </ul>
                             </details>
                        {% endif %}
                    {%- endfor -%}
                </ul>
            </details>
    {%- endif -%}
  {% endfor %}
{%- endif -%}
