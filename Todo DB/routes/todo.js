const express = require("express");
const router = express.Router();
const {
  getAllTodo,
  addTodo,
  removeTodo,
} = require("../controllers/todoController");

router.route("/").get(getAllTodo).post(addTodo);
router.route("/:id").delete(removeTodo);

module.exports = router;
