'''
Markdown_it Plugin for LunarKnights' markdown files
Author: Sachin
Date created: 09/30/2021
'''

from typing import MutableMapping, Sequence

from markdown_it.renderer import RendererHTML # type: ignore
from markdown_it.utils import OptionsDict # type: ignore
from markdown_it.token import Token # type: ignore

# Custom Markdown renderer
class LKRenderer(RendererHTML):
	
	def fence(
		self,
		tokens: Sequence[Token],
		idx: int,
		options: OptionsDict,
		env: MutableMapping,
	) -> str:

		token = tokens[idx]

		# add line numbers
		if token.info.endswith(' #'):
			token.info = token.info[:-2]
			token.attrPush(('class', 'line-numbers'))
			
			return super().fence(tokens, idx, options, env)

		original = super().fence(tokens, idx, options, env)

		# Change Mermaid code blocks to div tags
		if token.info.startswith('mermaid'):
			return f'<div class="mermaid">{token.content}</div>'

		return original
