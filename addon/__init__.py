from aqt import (
  mw,
  gui_hooks
)
from aqt.utils import tooltip
from aqt.operations.scheduling import suspend_cards
import aqt
config = aqt.mw.addonManager.getConfig(__name__)




def suspend_hard_new_card(review,card,ease):
  count_relapses_today = mw.col.db.scalar("select count() from revlog where ease = 1 and cid = ? and id > ?", card.id, (mw.col.sched.day_cutoff-86400)*1000) #86400 is the number of seconds in a day
  if count_relapses_today >= config["suspend_point"]:
    gui_hooks.reviewer_will_suspend_card(card.id)
    mw.col.sched.suspend_cards([card.id])
    tooltip(_("Card automatically suspended for being hard to learn"))
    note = card.note()
    note.add_tag("difficult_to_learn")
    note.flush()


gui_hooks.reviewer_did_answer_card.append(suspend_hard_new_card)
