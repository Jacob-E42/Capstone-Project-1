const BASE_URL = "http://localhost:5000";
const $editUserForm = $("#edit-user-form");

// async function deleteUser(user_id) {
// 	console.debug("deleteUser");
// 	const resp = await axios.delete(`${BASE_URL}/users/${user_id}`);
// 	const msg = resp.data.delete;
//     console.log(msg)
// 	return msg;
// }

$(".edit-user-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("EditUserButton: onSubmit");

	const target = $(evt.target);
	const user_id = target.data("user-id");

	let csrf_token = $("#csrf_token").val();
	let first_name = $("#first_name").val();
	let last_name = $("#last_name").val();
	let username = $("#username").val();
	let email = $("#email").val();
	let phone = $("#phone").val();

	let user = {
		csrf_token: csrf_token,
		first_name: first_name,
		last_name: last_name,
		username: username,
		email: email,
		phone: phone
	};

	const resp = await axios.patch(`${BASE_URL}/users/${user_id}`, user);

	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$(".delete-user-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("DeleteUserButton: onClick");
	const target = $(evt.target);
	const user_id = target.data("user-id");

	const resp = await axios.delete(`${BASE_URL}/users/${user_id}`);
	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$(".edit-task-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("EditTaskButton: onSubmit");

	const target = $(evt.target);
	const task_id = target.data("task-id");

	let csrf_token = $("#csrf_token").val();
	let title = $("#title").val();
	let description = $("#description").val();
	let resp_type = $("#resp_type").val();
	let due_time = $("#due_time").val();
	let is_completed = $("#is_completed").val();

	let task = {
		csrf_token: csrf_token,
		title: title,
		description: description,
		resp_type: resp_type,
		due_time: due_time,
		is_completed: is_completed
	};

	const resp = await axios.patch(`${BASE_URL}/tasks/${task_id}`, task);

	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$(".delete-task-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("DeleteTaskButton: onClick");
	const target = $(evt.target);
	const task_id = target.data("task-id");

	const resp = await axios.delete(`${BASE_URL}/tasks/${task_id}`);

	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$("input[type=checkbox]").ready(async function () {
	$("#remind_daily").val("");
	$("#notify_admin").val("");
});

$("input[type=checkbox]").change(async function (evt) {
	console.log("current value: ", $(evt.target).val());
	if (this.checked === true) {
		$(evt.target).val("y");
	} else {
		$(evt.target).val("");
	}
});

$(".edit-user-assignment-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("EditUserAssignmentButton: onSubmit");

	const target = $(evt.target);
	const user_id = target.data("user-id");
	const task_id = target.data("task-id");

	let csrf_token = $("#csrf_token").val();
	let remind_daily = $("#remind_daily").val();
	let notify_admin = $("#notify_admin").val();

	let assignment = {
		csrf_token: csrf_token,
		remind_daily: remind_daily,
		notify_admin: notify_admin
	};

	const resp = await axios.patch(`${BASE_URL}/assignments/users/${user_id}/${task_id}`, assignment);
	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$(".edit-task-assignment-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("EditUserAssignmentButton: onSubmit");

	const target = $(evt.target);
	const user_id = target.data("user-id");
	const task_id = target.data("task-id");

	let csrf_token = $("#csrf_token").val();
	let remind_daily = $("#remind_daily").val();
	let notify_admin = $("#notify_admin").val();

	let assignment = {
		csrf_token: csrf_token,
		remind_daily: remind_daily,
		notify_admin: notify_admin
	};

	const resp = await axios.patch(`${BASE_URL}/assignments/tasks/${task_id}/${user_id}`, assignment);
	window.location.replace(`${BASE_URL}/${resp.data}`);
});

$(".delete-assignment-button").on("click", async function (evt) {
	evt.preventDefault();
	console.debug("DeleteAssignmentButton: onClick");
	const target = $(evt.target);
	const task_id = target.data("task-id");
	const user_id = target.data("user-id");

	const resp = await axios.delete(`${BASE_URL}/assignments/${user_id}/${task_id}`);

	location.reload();
});

$(".completion-status-button").on("click", async function (evt) {
	console.debug("completion status button");
	const target = $(evt.target);
	const admin_id = target.data("admin-id");
	const task_id = target.data("task-id");

	const resp = await axios.post(`${BASE_URL}/notify/${task_id}/${admin_id}`);
	console.log(resp);
});
