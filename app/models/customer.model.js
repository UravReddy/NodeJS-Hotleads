const sql = require("./db.js");

// constructor
const Customer = function(customer) {
  

  this.email = customer.email;
  this.name = customer.name;
  this.phone_number = customer.phone_number;
  this.product = JSON.stringify(customer.product);

  this.vId=customer.product[0]['id'];
  this.vName=customer.product[0]['name'];
  this.vSelected=customer.product[0]['selected'];

  this.advertisingLeadSource = customer.advertisingLeadSource;
};

Customer.create = (newCustomer, result) => {
  if (newCustomer.phone_number === undefined || newCustomer.phone_number ===  ''){
    console.log(newCustomer.phone_number);
    console.log('Phone Number Issue');
    result(null,null);
  }else{
  sql.query("INSERT INTO hotleads2 SET ?", newCustomer, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);

      return;
    }

    console.log("created customer: ", { id: res.insertId, ...newCustomer });
    result(null, { id: res.insertId, ...newCustomer });
    
  });
}
};

Customer.findById = (customerId, result) => {
  sql.query(`SELECT * FROM hotleads2 WHERE id = ${customerId}`, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(err, null);
      return;
    }

    if (res.length) {
      console.log("found customer: ", res[0]);
      result(null, res[0]);
      return;
    }

    // not found Customer with the id
    result({ kind: "not_found" }, null);
  });
};

Customer.getAll = result => {
  sql.query("SELECT * FROM hotleads2", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log("hotleads2: ", res);
    result(null, res);
  });
};

Customer.updateById = (id, customer, result) => {
  sql.query(
    "UPDATE hotleads2 SET email = ?, name = ?, phone_number = ? WHERE id = ?",
    [customer.email, customer.name, customer.phone_number, id],
    (err, res) => {
      if (err) {
        console.log("error: ", err);
        result(null, err);
        return;
      }

      if (res.affectedRows == 0) {
        // not found Customer with the id
        result({ kind: "not_found" }, null);
        return;
      }

      console.log("updated customer: ", { id: id, ...customer });
      result(null, { id: id, ...customer });
    }
  );
};

Customer.remove = (id, result) => {
  sql.query("DELETE FROM hotleads2 WHERE id = ?", id, (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    if (res.affectedRows == 0) {
      // not found Customer with the id
      result({ kind: "not_found" }, null);
      return;
    }

    console.log("deleted customer with id: ", id);
    result(null, res);
  });
};

Customer.removeAll = result => {
  sql.query("DELETE FROM hotleads2", (err, res) => {
    if (err) {
      console.log("error: ", err);
      result(null, err);
      return;
    }

    console.log(`deleted ${res.affectedRows} hotleads2`);
    result(null, res);
  });
};

module.exports = Customer;
