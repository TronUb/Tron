from .create_group_call import CreateGroupCall
from .get_group_call import GetGroupCall
from .join_group_call import JoinGroupCall



class Phone(
    CreateGroupCall,
    GetGroupCall,
    JoinGroupCall
):
    pass
