import axios from 'axios';
import { apiEndPoint } from '../Config/api.js';

const instance = () => {
  return axios.create({
    baseURL: apiEndPoint,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${localStorage.getItem('token')}`,
    },
  });
};

export const authAPI = {
  createUser(body) {
    return instance()
      .post(`/user/create`, body)
      .then((response) => response);
  },
  createToken(body) {
    return instance()
      .post(`/user/token`, body)
      .then((response) => response.data);
  },
};

export const authorizedUserAPI = {
	updateUser(body, ) {
		return instance()
			.put(`/user/me`, body)
			.then((response) => response);
	},
	retrieveUser() {
		return instance()
			.get(`/user/me`)
			.then((response) => response.data)
	}
}

export const authorizedAttendanceAPI = {
	listCourses() {
		return instance()
			.get(`/attendance/courses/`)
			.then((response) => response);
	},
	listStudents() {
		return instance()
			.get(`/attendance/students`)
			.then((response) => response);
	},
	createCourse(body) {
		return instance()
			.post(`/attendance/courses/`, body)
			.then((response) => response);
	},
	updateCourse(body) {
		return instance()
			.put(`/attendance/courses/`, body)
			.then((response) => response);
	},
	retrieveCourse(courseId) {
		return instance()
			.get(`/attendance/courses/` + courseId)
			.then((response) => response);
	},
	retrieveCourseHistory(courseId) {
		return instance()
			.get(`/attendance/attendance/history`, { params: { course_id: courseId } })
			.then((response) => response);
	},
	deleteCourse(courseId) {
		return instance()
			.delete(`/attendance/courses/` + courseId)
			.then((response) => response);
	},
	startSession(courseId, file) {
		let formData = new FormData();

		formData.append('file', file);

		const config = {
			headers: {
				'content-type': 'multipart/form-data',
				Authorization: `Token ${localStorage.getItem('token')}`
			}
		}

		axios.post(apiEndPoint + '/attendance/courses/' + courseId + '/mark-attendance/', formData, config)
			.then((response) => response);
	}
}