---
layout: post
title: Cours
permalink: /school/
content-type: eg
---
<style>
summary {
	position: sticky;
	top: 0;
	background-color: white;
}
.container {
    padding-bottom: 190px;
}
.scroll-to-top {
    display: none
}
</style>
<main>
	{%- if page.permalink == "/school/" -%}
		<h1 style='text-align:center'> MENU </h1>
		{% assign mydocs = site.school | group_by: 'category' %}
		{% for cat in mydocs reversed%}
			{%- if cat.name != 'false' -%} 
				<details class="second">
					<summary>{{ cat.name | upcase }}</summary>
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
			{%- endif -%}
		{% endfor %}
	{%- endif -%}
</main>
