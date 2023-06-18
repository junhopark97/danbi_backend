def task_update_completion():
    pass


def subtask_update_completion():
    pass


# 이 함수들의 목적은
# 1. subtask의 is_complete = True로 변경하기 위해.
#   * 이 때, user.team이 subtask.team과 같아야 함. (다른 팀이면 에러메세지.)

# 2. 모든 하위 subtask의 값이 is_complete = True 이면, task의 is_complete 값도 True로 자동 변경.

# 여기서 중요한 점은 subtask의 is_complete를 수정할 때, 관련된 subtask의 값을 돌면서 확인!!
