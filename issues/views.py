import issues
from issues.models import CriticalIssue, Issue, LowPriorityIssue, Reporter
from issues.services.json_utils import read_json, write_json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

REPORTERS = "reporters.json"
ISSUES = "issues.json"

# ------------  REPORTERS -------------------#

@api_view(["GET"])
def get_reporters(request: Request) -> Response:
    reporters = read_json(REPORTERS)
    return Response(reporters, status = status.HTTP_200_OK)

@api_view(["GET"])
def get_reporter_details(request: Request, reporter_id: int) -> Response:
    reporters = read_json(REPORTERS)

    reporter_by_id = None
    for reporter in reporters:
        if reporter["id"] == reporter_id:
            reporter_by_id = reporter
            break

    if reporter_by_id is None:
        return Response(
            {'error': f"Reporter with id:{reporter_id}, was not found"},
            status= status.HTTP_404_NOT_FOUND
        )

    return Response(reporter_by_id)

@api_view(["POST"])
def create_reporter(request: Request) -> Response:
    reporters = read_json(REPORTERS)

    reporter_name = request.data.get("name")
    reporter_email = request.data.get("email")
    reporter_team = request.data.get("team")

    reporter_name_set = set()
    reporter_email_set = set()

    max_id = 0
    for reporter in reporters:
        max_id = max(reporter["id"], max_id)
        reporter_name_set.add(reporter["name"])
        reporter_email_set.add(reporter["email"])

    if reporter_name in reporter_name_set:
        return Response(
            f"error: {reporter_name} already exists in records",
            status= status.HTTP_400_BAD_REQUEST
        )

    if reporter_email in reporter_email_set:
        return Response(
            f"error: {reporter_email} already exists in records",
            status= status.HTTP_400_BAD_REQUEST
        )
    
    new_id = max_id + 1

    new_reporter = Reporter(id=new_id, name=reporter_name, email=reporter_email, team=reporter_team)

    try:
        new_reporter.validate()
    except ValueError as e:
        return Response(
            {'error': f"{str(e)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    reporters.append(new_reporter.to_dict())

    write_json(REPORTERS, reporters)

    return Response(new_reporter.to_dict(), status=status.HTTP_201_CREATED)

# ----------------- Issues ------------------- #

@api_view(["GET"])
def get_issues(request: Request) -> Response:
    issues = read_json(ISSUES)

    issue_id = request.GET.get("id")
    issue_status = request.GET.get("status")

    # If id found in query
    if issue_id:
        issue_by_id = None
        for issue in issues:
            if issue["id"] == int(issue_id):
                issue_by_id = issue
                break
    
        if issue_by_id is None:
            return Response(
                {"error": f"No issue found against id: {issue_id}"},
                status= status.HTTP_404_NOT_FOUND
            )
    
        return Response(issue_by_id)
    elif issue_status:
        issues_with_status = []
        for issue in issues:
            if issue["status"] == issue_status:
                issues_with_status.append(issue)

        if len(issues_with_status) == 0:
            return Response(
                {"error": f"No issues found against status :{issue_status}"},
                status= status.HTTP_404_NOT_FOUND
            )
        return Response(issues_with_status)

    # Else return complete list of issues
    return Response(issues, status= status.HTTP_200_OK)

@api_view(["POST"])
def create_issue(request: Request) -> Response:
    issues = read_json(ISSUES)

    issue_title = request.data.get("title")
    issue_description = request.data.get("description")
    issue_status = request.data.get("status")
    issue_priority = request.data.get("priority")
    issue_reporter_id = request.data.get("reporter_id")

    max_id = 0
    for issue in issues:
        max_id = max(max_id, issue["id"])
    
    new_id = max_id + 1

    if issue_priority == "critical":
        issue_instance = CriticalIssue(id=new_id, title=issue_title, description=issue_description, status=issue_status, priority=issue_priority, reporter_id=issue_reporter_id)
    elif issue_priority == "low":
        issue_instance = LowPriorityIssue(id=new_id, title=issue_title, description=issue_description, status=issue_status, priority=issue_priority, reporter_id=issue_reporter_id)
    else:
        issue_instance = Issue(id=new_id, title=issue_title, description=issue_description, status=issue_status, priority=issue_priority, reporter_id=issue_reporter_id)

    try:
        issue_instance.validate()
    except ValueError as e:
        return Response(
            {'error': f"{str(e)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    response_data = issue_instance.to_dict()

    issues.append(response_data)

    write_json(ISSUES, issues)

    response_data["message"] = issue_instance.describe()

    return Response(response_data, status= status.HTTP_201_CREATED)