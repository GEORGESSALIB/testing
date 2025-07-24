import csv

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import Computer, Assignee, ComputerHistory


def computer_list(request):
    computers = Computer.objects.all()
    return render(request, 'computer/computer_list.html', {'computers': computers})


# View to assign a computer to an assignee
def assign_computer(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)
    assignees = Assignee.objects.all()

    # Check if the computer is marked as spare
    if computer.spare:
        messages.error(request, "This computer is marked as spare and cannot be assigned.")
        return redirect('computer_list')

    if request.method == 'POST':
        assignee_id = request.POST.get('assignee')
        assignee = Assignee.objects.get(id=assignee_id)

        # Record the history of returning the computer if it's already assigned
        if computer.status == 'assigned':
            history = ComputerHistory(
                computer=computer,
                assignee=computer.assignee,
                action="Returned",
                timestamp=now()
            )
            history.save()

        # Now assign the computer
        computer.assignee = assignee
        computer.status = 'assigned'
        computer.save()

        # Create a new history record for the assignment
        ComputerHistory.objects.create(
            computer=computer,
            assignee=assignee,
            action="Assigned",
            timestamp=now()
        )

        return redirect('computer_list')

    return render(request, 'computer/assign_computer.html', {'computer': computer, 'assignees': assignees})

def return_computer(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)

    # Record the history of returning the computer
    history = ComputerHistory(
        computer=computer,
        assignee=computer.assignee,
        action="Returned",
    )
    history.save()

    # Update the computer status and clear the assignee
    computer.status = 'available'
    computer.assignee = None  # Clear the assignee
    computer.save()

    return redirect('computer_list')


def computer_history(request, computer_id):
    computer = get_object_or_404(Computer, pk=computer_id)
    history = computer.history.all()  # Fetch all history records for the computer

    return render(request, 'computer/computer_history.html', {'computer': computer, 'history': history})

def export_computers_csv(request):
    # Prepare the response for CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="computers.csv"'

    writer = csv.writer(response)
    writer.writerow(['Serial Number', 'Name', 'Specification', 'Components', 'Status', 'Assignee'])

    computers = Computer.objects.all()
    for computer in computers:
        writer.writerow([computer.serial_number, computer.name, computer.specification, computer.components,
                         computer.status, computer.assignee.name if computer.assignee else 'N/A'])

    return response

def export_computer_history_csv(request, computer_id):
    # Get the computer by ID
    computer = get_object_or_404(Computer, pk=computer_id)

    # Prepare the response for CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{computer.name}_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['Assignee', 'Action', 'Timestamp'])

    # Get the history records for the computer
    history = ComputerHistory.objects.filter(computer=computer)
    for record in history:
        writer.writerow([record.assignee.name if record.assignee else 'N/A', record.action, record.timestamp])

    return response