
import json
from langchain.tools import Tool

def user_info_tool_func(user_json: str) -> str:
    try:
        user = json.loads(user_json)
    except json.JSONDecodeError:
        return "사용자 정보를 불러오는 데 실패했습니다. JSON 형식을 확인해주세요."

    return (
        f"[사용자 정보]\n"
        f"solarspaceId: {user.get('solarspaceId')}\n"
        f"businessNumber: {user.get('businessNumber')}\n"
        f"firmName: {user.get('firmName')}\n"
        f"representativePhone: {user.get('representativePhone')}\n"
        f"plantName: {user.get('plantName')}\n"
        f"facilityConfirm: {user.get('facilityConfirm')}\n"
        f"facilityCode: {user.get('facilityCode')}\n"
        f"facilityCapa: {user.get('facilityCapa')}\n"
        f"facilityWeight: {user.get('facilityWeight')}\n"
        f"permitNumber: {user.get('permitNumber')}\n"
        f"permitCapa: {user.get('permitCapa')}\n"
        f"ppaContractTarget: {user.get('ppaContractTarget')}\n"
        f"ppaContractNumber: {user.get('ppaContractNumber')}\n"
        f"taxRegistrationId: {user.get('taxRegistrationId')}\n"
        f"ppaBranchOffice: {user.get('ppaBranchOffice')}\n"
        f"ppaContactPhone: {user.get('ppaContactPhone')}\n"
        f"recTradingType: {user.get('recTradingType')}\n"
        f"recContractTarget: {user.get('recContractTarget')}\n"
        f"commercialDate: {user.get('commercialDate')}\n"
        f"recStartDate: {user.get('recStartDate')}\n"
        f"subscription: {user.get('subscription')}\n"
        f"certificateExpiresAt: {user.get('certificateExpiresAt')}\n"
        f"representativeName: {user.get('representativeName')}\n"
        f"contactName: {user.get('contactName')}\n"
        f"contactPhone: {user.get('contactPhone')}\n"
        f"contactMail: {user.get('contactMail')}"
    )

user_info_tool = Tool(
    name="user_info_tool",
    func=user_info_tool_func,
    description="사용자의 발전소 정보, 계약 정보, 매출 정보 등을 조회하는 도구입니다. JSON 문자열을 입력받습니다."
)
