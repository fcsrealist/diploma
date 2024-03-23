import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar.js';
import Header from '../components/Header.js';
import {useNavigate} from 'react-router-dom';
import axios from 'axios';
import { authorizedAttendanceAPI } from '../Api/Requests';

function NewClass(props) {
	// States
	const [courseName, setCourseName] = useState('');
	const [students, setStudents] = useState([]);
	const [selectedStudent, setSelectedStudents] = useState([]);
	const history = useNavigate();

	function isAuthorized() {
		try {
			if (!localStorage.getItem('token')){
				history('/login')
			}
		} catch (error) {}
	}

	function handleStudentsList(e) {
		const updatedStudents = [...e.target.options]
			  .filter(option => option.selected)
			  .map(x => x.value);
		setSelectedStudents(updatedStudents);
	}

	const loadStudents = async () => {
		try {
			const { data } = await authorizedAttendanceAPI.listStudents();
			setStudents(data);
			console.log(data);
		} catch (error) {
			console.log(error);
		}
	};

	async function createClass(e) {
		e.preventDefault();
		let body = {
			name: courseName,
			student_ids: selectedStudent
		};

		try {
			await authorizedAttendanceAPI.createCourse(body);
			history('/');
		} catch (error) {
			console.log(error);
		}
	}

	useEffect(() => {
		isAuthorized();
		loadStudents()
	}, []);
	return (
		<>
			<Navbar />
			<div className="relative md:ml-64 p-1">
				<Header />
				<div className="relative bg-gradient-to-r from-gray-800 to-purple-900  md:pt-32 pb-32 pt-12 rounded-2xl">
					<div className="flex flex-wrap">
						<div className="w-full px-10">
							<div className="relative flex flex-col min-w-0 break-words bg-white rounded mb-6 xl:mb-0 shadow-lg">
								<div className="flex-auto p-4">
									<div className="flex flex-wrap">
										<div className=" w-full pr-4 max-w-full flex-grow flex-auto">
											<span className="flex justify-center uppercase text-purple-800 hover:text-yellow-500 mr-0 whitespace-no-wrap text-3xl font-bold p-4 px-0">
												Create a new class
											</span>
										</div>
									</div>
									<div class="flex flex-col px-80 mt-6 mb-4">
										<label class="flex flex-col justify-center">
											<span class="text-gray-600 font-semibold">Class/Course Name</span>
											<input
												type="text"
												onChange={(e) => setCourseName(e.target.value)}
												class="form-input mt-2 block focus:border-purple-800 rounded"
												placeholder="eg: CS-489 Diploma preparation"
											/>
										</label>
										<label class="flex flex-col mt-6">
											<span class="text-gray-600 font-semibold">
												Students in Class/Course
											</span>
											<select
												onChange={handleStudentsList}
												class="form-input mt-2 block focus:border-purple-800 rounded"
												placeholder=""
												multiple
											>
												{students.map((student, index) => (
													<option value={student.id}>{student.name}</option>
												))}
											</select>
										</label>

										<button
											class="mt-6 flex flex-col items-center px-2 py-4 rounded text-white cursor-pointer bg-purple-800 hover:bg-yellow-500 focus:border-white"
											onClick={(e) => createClass(e)}
										>
											<span class="font-semibold uppercase">Save</span>
										</button>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</>
	);
}
export default NewClass;
