const Todo = require("../models/Todo");
const { StatusCodes } = require("http-status-codes");
const { BadRequestError, NotFoundError } = require("../errors");

const getAllTodo = async (req, res) => {
  const todo = await Todo.find({ createdBy: req.user.userID }).sort("date");
  res.status(StatusCodes.OK).json({ todo, count: todo.length });
};

const addTodo = async (req, res) => {
  req.body.createdBy = req.user.userID;
  const todo = await Todo.create(req.body);
  res.status(StatusCodes.CREATED).json({ todo });
};

const removeTodo = async (req, res) => {
  // I am accessing the user object in the req object. Then accessing the userID property in the user object. The same is true for params. This is nested destructuring.
  const {
    user: { userID },
    params: { id: jobID },
  } = req;
  console.log(jobID);
  const todo = await Todo.findByIdAndRemove({ _id: jobID, createdBy: userID });
  if (!todo) {
    throw new NotFoundError(`No job with ${userID}`);
  }

  res.status(StatusCodes.OK).send();
};

module.exports = {
  getAllTodo,
  addTodo,
  removeTodo,
};
