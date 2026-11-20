package dao;

import java.sql.Connection;
import java.sql.DriverManager;

public class DAO {
    protected Connection con;

    public DAO() {
        if (con == null) {
            String dbUrl = "jdbc:sqlite:database/restman.db";
            try {
                Class.forName("org.sqlite.JDBC");
                con = DriverManager.getConnection(dbUrl);
            } catch (Exception e) {
                // Hỗ trợ cả MySQL nếu cần: "jdbc:mysql://localhost:3306/restman?useSSL=false"
                e.printStackTrace();
            }
        }
    }
}
