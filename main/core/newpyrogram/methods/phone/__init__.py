from .create_group_call import CreateGroupCall
from .get_group_call import GetGroupCall
from .join_group_call import JoinGroupCall
from .leave_group_call import LeaveGroupCall
from .edit_group_call_participant import EditGroupCallParticipant



class Phone(
    CreateGroupCall,
    GetGroupCall,
    JoinGroupCall,
    LeaveGroupCall,
    EditGroupCallParticipant
):
    pass
