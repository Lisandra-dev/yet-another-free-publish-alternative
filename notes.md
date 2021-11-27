---
layout: post
title: 
permalink: /notes/
content-type: eg
---
<style>
.category-content a {
    text-decoration: none;
    color: #4183c4;
}

.category-content a:hover {
    text-decoration: underline;
    color: #4183c4;
}

details {
	padding-left: 30px;
	padding-bottom: 12px;
	padding-top: 12px;

}

h1 {
	padding-left: 20px;
}

hr{
	color: #a1b3b9;
	width: 95%;
background-color: transparent;

}

hr.type1 {
	border-top: 3px dashed;
	border-bottom: 0;
	background-color: transparent;
}

details[open] {
	border-bottom: 0;
}

summary {
	position: sticky;
	top: 0;
	background-color: white;
}
.container {
    padding-bottom: 20%;
}
.scroll-to-top {
    display: none
}
</style>


<main>
	{%- if page.permalink == "/notes/" -%}
		<h1 style='text-align:center'> MENU </h1>
		{% assign mydocs = site.notes | group_by_exp: 'item', "item.category | downcase"  %}
		{% for cat in mydocs %}
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
