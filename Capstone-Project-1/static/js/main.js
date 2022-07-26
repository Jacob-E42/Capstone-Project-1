"use strict";

const BASE_URL = "http://localhost:5000";
const $body = $("body");
const $currentUserId = $("#current-user").data("user-id");
const $currentUserFirstAndLastName = $("#current-user").data("user-name");
const $currentUserIsAdmin = $("#current-user").data("is-admin");
const $currentUserIsLoggedIn = $("#current-user").data("is-authenticated");
const $navbar = $("nav");
const $navUsers = $("#navUsers");
const $navTasks = $("#navTasks");
const $navCreateTask = $("#navCreateTask");
const $navLogin = $("#navLogin");
const $navSignup = $("#navSignup");
const $navLogout = $("#navLogout");
const $navMyProfile = $("#navMyProfile");
const $showUserLink = $(".show-user-link");
const $myTasks = $(".my-tasks");
const $createUserButton = $(".create-user-button");
const $usernameErrorSpan = $(".username-error");
const $patchUserButton = $(".patch-user-button");
const $editUserButton = $(".edit-user-button");
const $editUserForm = $("#edit-user-form");
const $deleteUserPrompt = $(".delete-user-prompt");
const $deleteUserButton = $(".delete-user-button");
const $dueTime = $(".duetime");
const $createTaskButton = $(".create-task-button");
const $editTaskButton = $(".edit-task-button");
const $deleteTaskPrompt = $(".delete-task-prompt");
const $deleteTaskButton = $(".delete-task-button");
const $completionStatusButton = $(".completion-status-button");
const $assignTaskButton = $(".assign-task-button");
const $assignUserButton = $(".assign-user-button");
const $checkboxes = $("input[type=checkbox]");
const $editUserAssignmentButton = $(".edit-user-assignment-button");
const $editTaskAssigmentButton = $(".edit-task-assignment-button");
const $deleteAssignmentButton = $(".delete-assignment-button");
const $reassignButton = $(".reassign-button");
const $deleteAssignmentPrompt = $(".delete-assignment-prompt");
const $editUserAssignmentFormButton = $(".edit-user-assignment-form");
const $editTaskAssignmentFormButton = $(".edit-task-assignment-form");
const $remindDailyText = $(".remind-daily-text");
const $notifyAdminText = $(".notify-admin-text");
const $dailyReminderButton = $(".daily-reminder-button");
const $remindUserButton = $(".remind-user-button");
const $remindTaskButton = $(".remind-task-button");

async function start() {
	console.debug("start");

	await hideLoggedInUserComponents();
	let isLoggedIn = checkForLoggedInUser();
	let isAdmin;
	if ($currentUserIsAdmin) isAdmin = JSON.parse($currentUserIsAdmin.toLowerCase());
	if (isLoggedIn && isAdmin) showAdminUI();
	else if (isLoggedIn && !isAdmin) showRegularUserUI();
	else showAnonymousUserUI();
}

$(start);
