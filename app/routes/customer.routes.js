const customers = require("../controllers/customer.controller.js");
const { authJwt } = require("../middleware");

module.exports = function(app) {
app.use(function(req, res, next) {
  res.header(
    "Access-Control-Allow-Headers",
    "x-access-token, Origin, Content-Type, Accept"
  );
  next();
});

app.get("/customers/", customers.findAll);

app.post(
  "/customers/",
  [authJwt.verifyToken],
  customers.create
);

};
