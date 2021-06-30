# from app.utils.utils_of_security import get_password_hash

# db_additions = dict(
#     Human={
#         "hash_password": {"py_check": "get_password_hash"}
#     }
# )

from app.db._change_db._db_additions._base_additions import _raw_m, AddArrtInDbClass
from app.db._change_db._db_additions._human_addition import _raw_m
from app.db._change_db._db_additions._admin_addition import _raw_m
from app.db._change_db._db_additions._user_addition import _raw_m
from app.db._change_db._db_additions._smm_addition import _raw_m
from app.db._change_db._db_additions._direction_expert_addition import _raw_m
from app.db._change_db._db_additions._developer_addition import _raw_m

from app.db._change_db._db_additions._competition_direction_addition import _raw_m
from app.db._change_db._db_additions._competition_addition import _raw_m
from app.db._change_db._db_additions._criterion_addition import _raw_m
from app.db._change_db._db_additions._direction_addition import _raw_m
from app.db._change_db._db_additions._human_contacts_addition import _raw_m
from app.db._change_db._db_additions._mark_work_addition import _raw_m
from app.db._change_db._db_additions._page_addition import _raw_m
from app.db._change_db._db_additions._news_addition import _raw_m
from app.db._change_db._db_additions._question_addition import _raw_m
from app.db._change_db._db_additions._simple_entity_addition import _raw_m
from app.db._change_db._db_additions._task_addition import _raw_m
from app.db._change_db._db_additions._user_work_addition import _raw_m
