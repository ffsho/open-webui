from typing import List, Optional

from open_webui.internal.db import Base, get_db
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, Text

####################
# Prompts Suggestions DB Schema
####################


class PromptSuggestion(Base):
    __tablename__ = "prompts_suggestions"

    title = Column(String, primary_key=True)
    content = Column(Text)
    usage_count = Column(Integer, default=0)


class PromptSuggestionModel(BaseModel):
    title: str
    content: str
    usage_count: int = 0
    model_config = ConfigDict(from_attributes=True)


####################
# Forms
####################


class PromptSuggestionForm(BaseModel):
    title: str
    content: str


class PromptsSuggestionsTable:
    def get_all_suggestions(self) -> List[PromptSuggestionModel]:
        try:
            with get_db() as db:
                suggestions = db.query(PromptSuggestion).all()
                return [PromptSuggestionModel.model_validate(suggestion) for suggestion in suggestions]
        except Exception:
            return []

    def get_suggestion_by_title(self, title: str) -> Optional[PromptSuggestionModel]:
        try:
            with get_db() as db:
                suggestion = db.query(PromptSuggestion).filter_by(title=title).first()
                return PromptSuggestionModel.model_validate(suggestion) if suggestion else None
        except Exception:
            return None

    def add_suggestion(self, form_data: PromptSuggestionForm) -> Optional[PromptSuggestionModel]:
        try:
            with get_db() as db:
                suggestion = PromptSuggestion(
                    title=form_data.title,
                    content=form_data.content,
                    usage_count=0
                )
                db.add(suggestion)
                db.commit()
                db.refresh(suggestion)
                return PromptSuggestionModel.model_validate(suggestion)
        except Exception:
            return None

    def update_suggestion(self, title: str, form_data: PromptSuggestionForm) -> Optional[PromptSuggestionModel]:
        try:
            with get_db() as db:
                suggestion = db.query(PromptSuggestion).filter_by(title=title).first()
                if suggestion:
                    suggestion.title = form_data.title
                    suggestion.content = form_data.content
                    db.commit()
                    return PromptSuggestionModel.model_validate(suggestion)
                return None
        except Exception:
            return None

    def delete_suggestion(self, title: str) -> bool:
        try:
            with get_db() as db:
                db.query(PromptSuggestion).filter_by(title=title).delete()
                db.commit()
                return True
        except Exception:
            return False

    def get_usage_count(self, title: str) -> Optional[int]:
        try:
            with get_db() as db:
                suggestion = db.query(PromptSuggestion).filter_by(title=title).first()
                return suggestion.usage_count if suggestion else None
        except Exception:
            return None

    def increment_usage_count(self, title: str) -> bool:
        try:
            with get_db() as db:
                suggestion = db.query(PromptSuggestion).filter_by(title=title).first()
                if suggestion:
                    suggestion.usage_count += 1
                    db.commit()
                    return True
                return False
        except Exception:
            return False

    def set_default_prompts_suggestions(self) -> None:
        try:
            with get_db() as db:
                count = db.query(PromptSuggestion).count()
                if count > 0:
                    return
                default_suggestions = [
                    {
                        "title": "Help me study vocabulary for a college entrance exam",
                        "content": "Help me study vocabulary: write a sentence for me to fill in the blank, and I'll try to pick the correct option.",
                    },
                    {
                        "title": "Give me ideas for what to do with my kids' art",
                        "content": "What are 5 creative things I could do with my kids' art? I don't want to throw them away, but it's also so much clutter.",
                    },
                    {
                        "title": "Tell me a fun fact about the Roman Empire",
                        "content": "Tell me a random fun fact about the Roman Empire",
                    },
                    {
                        "title": "Show me a code snippet of a website's sticky header",
                        "content": "Show me a code snippet of a website's sticky header in CSS and JavaScript.",
                    },
                    {
                        "title": "Explain options trading if I'm familiar with buying and selling stocks",
                        "content": "Explain options trading in simple terms if I'm familiar with buying and selling stocks.",
                    },
                    {
                        "title": "Overcome procrastination give me tips",
                        "content": "Could you start by asking me about instances when I procrastinate the most and then give me some suggestions to overcome it?",
                    },
                ]
                
                for suggestion_data in default_suggestions:
                    existing = db.query(PromptSuggestion).filter_by(title=suggestion_data["title"]).first()
                    if not existing:
                        suggestion = PromptSuggestion(
                            title=suggestion_data["title"],
                            content=suggestion_data["content"],
                            usage_count=0
                        )
                        db.add(suggestion)
                
                db.commit()
        except Exception as e:
            print(f"Error setting default prompt suggestions: {e}")


PromptsSuggestions = PromptsSuggestionsTable()