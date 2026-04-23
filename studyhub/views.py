"""
Study Hub views — Browse, Upload, Download, Vote.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import FileResponse
from .models import Resource, ResourceVote
from .forms import ResourceUploadForm


def resource_list(request):
    """Browse/search study hub resources."""
    resources = Resource.objects.select_related('uploader')

    # Search
    query = request.GET.get('q', '')
    if query:
        resources = resources.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(subject__icontains=query) |
            Q(tags__icontains=query) |
            Q(course__icontains=query)
        )

    # Category filter
    category = request.GET.get('category', '')
    if category:
        resources = resources.filter(category=category)

    # Sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'popular':
        resources = resources.order_by('-download_count')
    elif sort == 'votes':
        resources = resources.order_by('-upvotes')
    elif sort == 'verified':
        resources = resources.filter(is_verified=True)
    else:
        resources = resources.order_by('-created_at')

    categories = Resource.CATEGORY_CHOICES

    context = {
        'resources': resources,
        'query': query,
        'category': category,
        'sort': sort,
        'categories': categories,
    }
    return render(request, 'studyhub/list.html', context)


def resource_detail(request, pk):
    """View resource details."""
    resource = get_object_or_404(Resource.objects.select_related('uploader'), pk=pk)
    user_vote = None
    if request.user.is_authenticated:
        user_vote = ResourceVote.objects.filter(resource=resource, user=request.user).first()

    context = {
        'resource': resource,
        'user_vote': user_vote,
    }
    return render(request, 'studyhub/detail.html', context)


@login_required
def resource_upload(request):
    """Upload a new study resource."""
    if request.method == 'POST':
        form = ResourceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploader = request.user
            resource.save()
            messages.success(request, 'Resource uploaded successfully! 📚')
            return redirect('studyhub:detail', pk=resource.pk)
    else:
        form = ResourceUploadForm()

    return render(request, 'studyhub/upload.html', {'form': form})


@login_required
def resource_download(request, pk):
    """Download a resource file."""
    resource = get_object_or_404(Resource, pk=pk)
    resource.download_count += 1
    resource.save(update_fields=['download_count'])
    return FileResponse(resource.file.open('rb'), as_attachment=True, filename=resource.file.name.split('/')[-1])


@login_required
def resource_vote(request, pk, vote_type):
    """Upvote or downvote a resource."""
    resource = get_object_or_404(Resource, pk=pk)

    if resource.uploader == request.user:
        messages.error(request, "You can't vote on your own resource.")
        return redirect('studyhub:detail', pk=pk)

    existing_vote = ResourceVote.objects.filter(resource=resource, user=request.user).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Remove vote
            if vote_type == 'up':
                resource.upvotes = max(0, resource.upvotes - 1)
            else:
                resource.downvotes = max(0, resource.downvotes - 1)
            existing_vote.delete()
            resource.save()
            messages.info(request, 'Vote removed.')
        else:
            # Switch vote
            if existing_vote.vote_type == 'up':
                resource.upvotes = max(0, resource.upvotes - 1)
                resource.downvotes += 1
            else:
                resource.downvotes = max(0, resource.downvotes - 1)
                resource.upvotes += 1
            existing_vote.vote_type = vote_type
            existing_vote.save()
            resource.save()
            messages.success(request, 'Vote updated.')
    else:
        ResourceVote.objects.create(resource=resource, user=request.user, vote_type=vote_type)
        if vote_type == 'up':
            resource.upvotes += 1
        else:
            resource.downvotes += 1
        resource.save()
        messages.success(request, 'Vote recorded! 👍' if vote_type == 'up' else 'Vote recorded.')

    # Auto-verify if upvotes reach threshold
    if resource.upvotes >= 5 and not resource.is_verified:
        resource.is_verified = True
        resource.save()

    return redirect('studyhub:detail', pk=pk)
