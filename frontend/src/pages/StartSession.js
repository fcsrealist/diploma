import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar.js';
import Header from '../components/Header.js';
import {useNavigate} from 'react-router-dom';
import { authorizedAttendanceAPI } from '../Api/Requests';
import { useParams } from "react-router-dom";

function StartSessionClass(props) {
	const params = useParams()

	// States
	const [course, setCourse] = useState({});
	const [file, setFile] = useState([]);
	const history = useNavigate();

	function isAuthorized() {
		try {
			if (!localStorage.getItem('token')){
				history('/login')
			}
		} catch (error) {}
	}

	const handleFileChange = (e) => {
		if (e.target.files) {
		  setFile(e.target.files[0]);
		}
	};

	const loadCourse = async () => {
		try {
			const { data } = await authorizedAttendanceAPI.retrieveCourse(params.id);
			setCourse(data);
			console.log(data);
		} catch (error) {
			console.log(error);
		}
	};

	async function startSession(e) {
		if (file){
			e.preventDefault();
			const { data } = await authorizedAttendanceAPI.startSession(params.id, file);

			history('/')
		}
	}

	useEffect(() => {
		isAuthorized();
		loadCourse();
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
											<h5 className="text-gray-800 uppercase font-bold text-lg">
												{course.name}
											</h5>
										</label>
										<label className="flex flex-col justify-center">
											<span className="text-gray-600 font-semibold">Load file</span>
											<input
												type="file"
												onChange={handleFileChange}
												className="form-input mt-2 block focus:border-purple-800 rounded"
												placeholder="eg: CS-489 Diploma preparation"
											/>
										</label>

										<button
											class="mt-6 flex flex-col items-center px-2 py-4 rounded text-white cursor-pointer bg-purple-800 hover:bg-yellow-500 focus:border-white"
											onClick={(e) => startSession(e)}
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
export default StartSessionClass;
